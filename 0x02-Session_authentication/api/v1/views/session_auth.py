#!/usr/bin/env python3
""" Module for session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, session, Response
from models.user import User
from os import getenv
from typing import List


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login

    Give user credentials for login.
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not pwd:
        return jsonify({"error": "password missing"}), 400

    user: List= User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        user: User= user[0]

    if user.is_valid_password(pwd) is False:
        return jsonify({"error": "wrong password"}), 404

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    cookie_name = getenv('SESSION_NAME')

    json_user = user.to_json()
    response: Response = jsonify(json_user)

    response.set_cookie(cookie_name, session_id)

    return response
