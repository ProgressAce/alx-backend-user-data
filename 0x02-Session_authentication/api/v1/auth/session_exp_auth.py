#!/usr/bin/env python3
""" Implement SessionAuth authentication that can expire. """

from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Implement SessionAuth authentication with expiration."""

    def __init__(self):
        """initialising authentication instance."""

        self.session_duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(self.session_duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID using <user_id> and parent method

        Arg:
            user_id: the id of the user.

        Returns:
            the created session ID."""

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id, "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user ID based on the session ID.

        Arg:
            session_id: the session ID.

        Return:
            the user ID from the session dictionary."""

        if not session_id:
            return None

        session_dict: dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict['user_id']

        created_at = session_dict.get('created_at')
        if not created_at:
            return None

        # if the session already expired then no need to return the user ID
        time_left: datetime = created_at + \
            timedelta(seconds=self.session_duration)
        present: datetime = datetime.now()

        if time_left < present:
            return None

        return session_dict['user_id']
