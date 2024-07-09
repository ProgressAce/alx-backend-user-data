#!/usr/bin/env python3
"""
Definition of a Basic Auth system.
"""

import base64
import binascii
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Implementation of a Basic Auth system.
    """

    def extract_base64_authorization_header(self, authorization_header: str) \
            -> str:
        """ Returns the authorization (auth) header's value.
        It is intended that the value be a base64 one, but it extracts any
        given value regardless.

        The auth header's value needs to start with the `Basic ` substring.
        The string value following this is the extracted value.

        The method assumes that authorization_header contains only one `Basic `
        """
        if not authorization_header:
            return None

        # ensure the argument is a string that starts with ...
        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        base64_str = authorization_header.strip('Basic ')
        return base64_str

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ Returns the decoded value of a base64 str.

        The decoded value is return as a utf-8 string.

        Returns:
          - The decoded base64 str as utf-8
          - None, if the argument is not a valid base64
        """
        if not base64_authorization_header:
            return None

        # ensure the argument is a string
        if not isinstance(base64_authorization_header, str):
            return None

        decoded_auth_value = ''
        try:
            byte_base64 = base64.b64decode(base64_authorization_header)
            decoded_auth_value = byte_base64.decode('utf-8')
        except binascii.Error:
            return None

        return decoded_auth_value

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Returns the user email and password from the Base64 decoded value.

        The argument should be a string that contains `:`. The `:` is used to
        separate the user email and password.
        This method returns 2 values

        The method accepts decoded_base64_authorization_header with a password
        containing `:`, but assumes that the email does not include one.
        """
        if not decoded_base64_authorization_header:
            return None

        # ensure the argument is a string and contains `:`
        if not isinstance(decoded_base64_authorization_header, str):
            return None

        if ':' not in decoded_base64_authorization_header:
            return None

        credentials = decoded_base64_authorization_header.split(':', 1)
        email = credentials[0]
        pwd = credentials[1]

        return (email, pwd)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password.

        Dependencies:
          - the search method of the app's User model.
          - the is_valid_password method of the app's User model.
        """
        if not user_email or not isinstance(user_email, str):
            return None

        if not user_pwd or not isinstance(user_pwd, str):
            return None

        user_list = User.search({'email': user_email})
        # when no user is found
        if len(user_list) == 0:
            return None

        user: User = user_list[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user
