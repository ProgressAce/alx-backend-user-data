#!/usr/bin/env python3
"""
Module for the Flask app.
"""
from auth import Auth
from flask import Flask, abort, jsonify, request, Response, Request, redirect


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """GET /
    Returns:
      - {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """POST /users
    Registers a new user to the app.

    Returns:
      - 201 status, upon successful addition to the app.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "<email> is missing"}), 400

    if not password:
        return jsonify({"error": "<password> is missing"}), 400

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """POST /sessions

    Authenticate login credentials and if valid then
    a session is created for the user.

    Returns:
      - 200 status, for successful login.
      - 401 status, for invalid credentials.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401, description="Authentication requirements not met")

    if not AUTH.valid_login(email, password):
        abort(401, description="Authentication requirements not met")

    session_id: str = AUTH.create_session(email)

    response: Response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /sessions
    Sign-out an user by deleting the existing session id.

    Returns:
      - 200 status, everything went okay.
      - 403 status, if the user does not exist
    """
    session_id: str = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/', code=302)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """GET /profile

    Requires Authorization (session id as a cookie).
    Provides the user's email address.
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """POST /reset_password

    Requires authorization.
    Generates and returns a reset token.
    Returns:
      - 200 status + json payload, for success.
      - 403 status, for unauthorized access.
    """
    email = request.form.get('email')

    reset_token: str = AUTH.get_reset_password_token(email)
    if not reset_token:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """PUT /reset_password

    Updates the user's password if the reset token is correct.
    Returns:
      - 403 status, if the token or form data is invalid.
      - 200 status + json payload, for valid token.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
