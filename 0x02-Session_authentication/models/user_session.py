#!/usr/bin/env python3
"""Creates a model/structure for associating a user and session."""

from models.base import Base


class UserSession(Base):
    """Associates a user with a session."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialising an instance."""

        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
