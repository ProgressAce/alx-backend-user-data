#!/usr/bin/
"""Manages API authentication."""

from flask import request as req
from typing import List, TypeVar


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
        """Validates requests to secure the API."""

        if request is None or not request.get("Authorization"):
            return None

        return request.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """doc"""
        return None
