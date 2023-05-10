#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request
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
        Auth.register_user(email, password)
        message = {"email": f"{email}", "message": "user created"}
        return jsonify(message)
    except ValueError:
        return jsonify({"message": "email already registered"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
