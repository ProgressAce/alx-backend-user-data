#!/usr/bin/env python3
""" Module of SessionAuth views
"""

from os import getenv
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """ POST /auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """

    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400

    user_list: User = User.search({"email": email})
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404
    user = user_list[0]

    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """ DELETE /auth_session/logout

    Returns:
      - empty JSON if the session has been deleted successfully
        with a 200 status code.
      - 404 if unsuccessful
    """

    from api.v1.app import auth

    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)

    return jsonify({}), 200
