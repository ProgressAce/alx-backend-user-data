#!/usr/bin/env python3
"""Manages API authentication."""

from typing import List, TypeVar
from flask import request as req


class Auth:
    """Handles API authentication."""

    def require_auth(self, path: str, exluded_paths: List[str]) -> bool:
        """Defines which routes don't need authentication.

        It is assumed that <excluded_paths> always contains a string paths
        ended by '/' or an '*' wildcard.
        The '*', allows zero or more of any character to be followed after it.

        Example for excluded_paths = ["/api/v1/stat*"]:
            - /api/v1/users will return True
            - /api/v1/status will return False
            - /api/v1/stats will return False

        Args:
            path: the route
            excluded_paths: the paths which don't require authentication.
        """

        # checking for empty arguments
        if path is None:
            return True

        if exluded_paths is None or len(exluded_paths) == 0:
            return True

        for excl_path in exluded_paths:
            if not isinstance(excl_path, str):
                return True

            # case of slash tolerant path
            # ( /api/v1/stats == /api/v1/stats/ )
            if excl_path[-1] == '/':
                slash_path = path + "/" if path[-1] != "/" else path

                if slash_path not in exluded_paths:
                    return True

                return False

            # case of a '*' ended excluded path
            if excl_path[-1] == '*':
                end_index = excl_path.find('*')

                if path[:end_index] != excl_path[:end_index]:
                    return True

                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Validates requests to secure the API.

        Arg:
            request: the request sent to the flask server.

        Returns:
            the authorization of a request, otherwise None."""

        if request is None or not request.headers.get("Authorization"):
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Validates the current user."""
        return None
