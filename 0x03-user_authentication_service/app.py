#!/usr/bin/env python3
"""Web server Flask set up."""

from auth import Auth
from flask import abort, Flask, jsonify, request, Response
from typing import Dict

AUTH = Auth()
app: Flask = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Returns a message for index route '/'.

    response - message: Bienvenue"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user_registration():
    """ POST /users
    JSON body:
      - email
      - password
    Return:
      if user already registered, a JSON represented informing message.
      code 400
      if user does not exist, a JSON represented confirmation message.
      code 200
    """

    # TODO: when sending the same curl request, it results in an exception
    # it has to do with the use of the same session object even after commiting

    error_msg: str = None

    email = request.form.get('email')
    password = request.form.get('password')

    # TODO: validate form data
    # use/return them for more detailed error messages

    try:
        user = AUTH.register_user(email, password)

        # None is returned if the given arguments/form data were invalid
        if not user:
            return jsonify({"message": "missing email and/or password"}), 400

        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ POST /sessions
    to login.
    JSON body:
      - email
      - password
    Return:
      * 401 status for incorrect login information.
      * 200 ....."""

    email: str = request.form.get('email')
    password: str = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id: str = AUTH.create_session(email)
    if not session_id:  # not entirely necessary
        abort(401)

    response: Response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response, 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
