#!/usr/bin/env python3
"""
Module for the Flask app.
"""
from auth import Auth
from flask import Flask, abort, jsonify, request, Response


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
