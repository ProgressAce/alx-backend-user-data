#!/usr/bin/env python3
"""Manages API authentication."""

from typing import List, TypeVar
from flask import request as req
from os import getenv


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
        """Checks that a request has an Authorization header.

        Arg:
            request: the request sent to the flask server.

        Returns:
            the authorization header's value of the request, otherwise None."""

        if request is None or not request.headers.get("Authorization"):
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Validates the current user."""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request.

        Arg:
            request: the http request.

        Returns the value of the cookie named according to env variable
        <SESSION_NAME>."""

        if request is None:
            return None

        session_name: str = getenv('SESSION_NAME')
        cookie_val = request.cookies.get(session_name)

        return cookie_val
