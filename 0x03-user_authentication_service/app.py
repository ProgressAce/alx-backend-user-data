#!/usr/bin/env python3
"""Web server Flask set up."""

from auth import Auth
from user import User
from flask import abort, Flask, jsonify, redirect, request, Response

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

    # TODO: fix bug - repeating this request causes an exception with
    # this and other routes.
    # it has to do with the use of the same session object even commiting

    error_msg: str = None

    email: str = request.form.get('email')
    password: str = request.form.get('password')

    # TODO: validate form data
    # use/return them for more detailed error messages

    try:
        user: User = AUTH.register_user(email, password)

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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /sessions

    Request is expected to have a cookie with session_id as key
    and a session ID its value.

    The user with requested session ID is found, their session is destroyed
    and the user is then redirected to GET /

    Returns:
      - 200, if the session discard and redirect were successful.
      - 403, if the user does not exist.
    """

    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)  # Forbidden

    try:
        AUTH.destroy_session(user.id)
    except ValueError:
        abort(403)  # ValueError occured during session discard

    return redirect('/', code=302)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def user_profile():
    """ GET /profile

    session_id cookie is expected with the request.
    Return:
      - 200, with JSON payload if user exists.
      - 403, if user or session ID does not exist.
    """

    # TODO: fix bug: the route cannot be repeated without an exception
    # being raised.
    # likely has to to with sqlalchemy session not being reset properly

    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)  # Forbidden

    return jsonify({"email": user.email}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
