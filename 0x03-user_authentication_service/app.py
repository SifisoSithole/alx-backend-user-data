#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, abort, url_for, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def entry():
    """
    return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    Create a new user
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        AUTH.register_user(email, password)
        message = {"email": "{}".format(email), "message": "user created"}
        return jsonify(message)
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'])
def login():
    """
    login user and create a sesion
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    logouts out the user and destroy session
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('entry'))


@app.route('/profile', methods=['GET'])
def profile():
    """
    returns user profile with email
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"})
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    returns reset password token
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    resets password and updates it
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify(
            {"email": f"{email}", "message": "Password updated"}
        )
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
