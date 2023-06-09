#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def log():
    """
    validates user credentials
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(getenv('SESSION_NAME'), session_id)
        return response
    else:
        return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def logout():
    """
    delete a session
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
