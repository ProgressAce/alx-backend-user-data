#!/usr/bin/env python3
"""Implements a SessionAuth authentication system."""

import uuid
from api.v1.auth.auth import Auth
from typing import Dict


class SessionAuth (Auth):
    """Defines the SessionAuth authentication mechanism."""

    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a <user_id>.

        Arg:
            user_id: string id of a user."""

        if user_id is None or type(user_id) != str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
