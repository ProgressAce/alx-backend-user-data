#!/usr/bin/env python3
"""Implements a SessionAuth authentication system."""

import uuid
from typing import Dict
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth (Auth):
    """Defines the SessionAuth authentication mechanism."""

    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a <user_id>.

        Used for storing a session_id based on its link with user_id

        Arg:
            user_id: string id of a user."""

        if user_id is None or type(user_id) != str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID.

        Used for retrieving a user_id based on its link with a session_id

        Arg:
            session_id: the session id."""

        if session_id is None or type(session_id) != str:
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value.

        Arg:
            request: the http request."""

        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)

        user = User.get(user_id)

        return user

    def destroy_session(self, request=None):
        """Deletes the user session / logout.

        Arg:
        request: the http request."""

        if request is None:
            return False

        cookie_session_id = self.session_cookie(request)
        if not cookie_session_id:
            return False

        user_id = self.user_id_for_session_id(cookie_session_id)
        if not user_id:
            return False

        self.user_id_by_session_id.pop(cookie_session_id)
        return True
