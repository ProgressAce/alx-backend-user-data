#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
import os
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized request handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden request handler"""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.before_request
def filter_request_beforehand():
    """Filters each request before passing it as route."""

    if auth:
        # request path is part of excluded list then it authen... won't occur
        if auth.require_auth(
            request.path,
            ["/api/v1/status/", "/api/v1/unauthorized/", "/api/v1/forbidden/"],
        ):

            if auth.authorization_header(request) is None:
                abort(401)

            current_user = auth.current_user(request)
            if current_user is None:
                abort(403)

            request.current_user = current_user


if __name__ == "__main__":
    # determine the authentication type
    auth_type = getenv("AUTH_TYPE")
    if auth_type == "auth":
        from api.v1.auth.auth import Auth

        auth = Auth()

    if auth_type == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth

        auth = BasicAuth()

    if auth_type == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth

        auth = SessionAuth()

    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
