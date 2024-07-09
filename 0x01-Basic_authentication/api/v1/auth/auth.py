#!/usr/bin/env python3
"""
App's Authentication system
"""
from typing import TypeVar, List
from flask import request as req


class Auth:
    """ Implementation of a Basic Authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if an url path requires authentication.

        The path is exempted if it is part of the excluded_paths list.
        Methods assumes that excluded_paths contains string paths always ending
        by a `/`.
        A url path is slash tolerant.
        (/api/v1/status and /api/v1/status/) both return False.

        Returns:
          - True, if the path needs it
          - False, if the path is exempted
        """
        if not path or not excluded_paths:
            return True

        # so paths can be slash tolerant
        if path[-1] == '/':
            slashed_path = path
        else:
            slashed_path = path + '/'

        if slashed_path in excluded_paths:
            return False

        return True

    def authorization_header(self, request: TypeError('req') = None) -> str:
        """ Retrieves the authorization header of a request.
        Returns:
          - None, if the Authorization header is not found
          - the Authorization header's value.
        """
        if request is None:
            return None

        auth_header = req.headers.get('Authorization')

        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request: TypeError('req') = None) \
            -> TypeVar('User'):
        """ NEEDS to be implemented.
        """
        return None
