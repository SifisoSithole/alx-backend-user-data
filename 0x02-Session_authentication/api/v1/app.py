#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from werkzeug.exceptions import Unauthorized, Forbidden


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth = getenv('AUTH_TYPE')

if auth == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def authentication():
    """
    Authorize before each request
    """
    if auth is None:
        returnNone

    result = auth.require_auth(
        request.path,
        ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    )
    if not result:
        return

    result = auth.authorization_header(request)
    if result is None:
        abort(401)

    result = auth.current_user(request)
    if result is None:
        abort(403)
    request.current_user = result


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(Unauthorized)
def unauthorized(error: Unauthorized) -> str:
    """
    unauthorized acccess
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(Forbidden)
def forbidden(error: Forbidden):
    """
    forbidenn access
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
