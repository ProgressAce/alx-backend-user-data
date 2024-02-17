#!/usr/bin/env python3
"""Creates a model/system to persist session data."""

from typing import Dict
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Defines a storage model to store session data."""

    # Possibly REMOVE
    # session_storage: Dict[str, UserSession] = {}

    def create_session(self, user_id=None):
        """Creates a session ID and associates it to user ID.

        OVERLOADS by ensuring that UserSession instance is included in
        the database.

        Arg:
            user_id: the ID of the user.
        Returns:
            the session ID."""

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # adding a user_session instance to DB for one place access
        user_session = UserSession(
            user_id=user_id, session_id=session_id)

        self.user_id_by_session_id[session_id].update(
            {"user_session": user_session}
        )

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user ID linked with with session ID in the session DB.

        Does so by requesting the UserSession instance in the database based on
        the session ID.

        Arg:
            session_id: the ID of the session."""

        user_id = super().user_id_for_session_id(session_id)
        if not user_id:
            return None

        session_dict: dict = self.user_id_by_session_id.get(session_id)

        user_session = session_dict.get("user_session")
        if not user_session:
            return None

        user_id: int = user_session.user_id

        return user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID.

        The session ID coming from the request cookie.

        Arg:
            request: the request."""

        # retrieve the session_id from a specific cookie of the request
        cookie_value = self.session_cookie(request)

        if not cookie_value:
            return False

        self.user_id_by_session_id.pop(cookie_value)
        return True
