#!/usr/bin/env python3
"""Web server Flask set up."""

from auth import Auth
from flask import Flask, jsonify, request
from typing import Dict

AUTH = Auth()
app: Flask = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Returns a message for index route '/'.

    response - message: Bienvenue"""
    return jsonify({"message": "Bienvenue"})


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

    r_json: Dict = None
    error_msg: str = None

    email = request.form.get('email')
    password = request.form.get('password')

    # TODO: validate form data
    # use/return them for more detailed error messages

    try:
        user = AUTH.register_user(email, password)

        # None is returned if the given arguments/form data were invalid
        if not user:
            return jsonify({"message": "missing email and/or password"})

        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
