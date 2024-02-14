#!/usr/bin/env python3
"""Manages API authentication."""

from typing import List, TypeVar
from flask import request as req


class Auth:
    """Handles API authentication."""

    def require_auth(self, path: str, exluded_paths: List[str]) -> bool:
        """Defines which routes don't need authentication.

        It is assumed that <excluded_paths> always contains string paths
        ended by '/'.

        Args:
            path: the route
            excluded_paths: the paths which don't require authentication.
        """

        # checking for empty arguments
        if path is None:
            return True

        if exluded_paths is None or len(exluded_paths) == 0:
            return True

        # slash tolerant path (can be /api/v1/stats or /api/v1/stats/)
        slash_path = path + "/" if path[-1] != "/" else path

        if slash_path not in exluded_paths:
            return True

        return False

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
