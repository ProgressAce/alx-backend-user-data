#!/usr/bin/env python3
"""
Session authentication system
"""
from api.v1.auth.auth import Auth
from models.user import User
from flask import Request
from uuid import uuid4


class SessionAuth(Auth):
    """ Session Authentication mechanism of the app.
    """
    # in-memory session ID storage
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id.

        Depends on the uuid model to create a session ID.
        """
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID.
        (Uses a session id to find a user id).

        Arg:
            session_id(str): the session id belonging to a certain user.

        Returns:
          - the user id, should the session id be found in the storage.
          - None, if the session ID fails validation,
            or if user_id is not found.
        """
        if not session_id or not isinstance(session_id, str):
            return None

        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        if not user_id:
            return None

        return user_id

    def current_user(self, request: Request = None):
        """ Returns a User instance based on a cookie value.

        This allows a User to be retrieved using a session id.

        Returns:
          - the user instance based on the cookie value if found.
          - None, if the user is not found or if the request argument is
          is valid.
        """
        if not request:
            return None

        session_id = SessionAuth.session_cookie(self, request)
        user_id = SessionAuth.user_id_for_session_id(self, session_id)

        if not session_id or not user_id:
            return None

        user = User.get(user_id)

        return user
