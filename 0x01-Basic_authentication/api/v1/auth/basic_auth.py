#!/usr/bin/env python3
"""Implements a Basic Authentication system."""

import base64
import binascii
from typing import TypeVar, List
from api.v1.auth.auth import Auth
from models.base import DATA
from models.user import User


class BasicAuth(Auth):
    """Implements a BasicAuthentication system."""

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """Returns the Base64 part of the Authorization header.

        It is assumed that <authorization_header> contains only one 'Basic'.

        Arg:
            authorization_header: the authorization header's value."""

        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Returns the decoded value of a Base64 string arg.

        Arg:
            base64_authorization_header: a Base64 string argument."""

        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_base64 = base64.b64decode(base64_authorization_header)

            return decoded_base64.decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value.

        It is assumed that <decoded_base64_authorization_header>, the decoded
        base64 string will contain one ':' that will differentiate the email
        and the password. The password is allowed to consist of ':' characters.

        Arg:
            decoded_base64_authorization_header: the decoded base64 value."""

        no_details = (None, None)

        if decoded_base64_authorization_header is None:
            return no_details
        if not isinstance(decoded_base64_authorization_header, str):
            return no_details
        if ':' not in decoded_base64_authorization_header:
            return no_details

        # seperate email and password parts from the decoded base64 string
        split_str = decoded_base64_authorization_header.split(':', 1)

        return (split_str[0], split_str[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """Returns the User instance based on his email and password.

        Args:
            user_email: the user's email.
            user_pwd: the user's password."""

        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        # validate that there is an existing user in the database.
        if DATA.get(User.__name__) is None:
            return None

        # looks for any User instance with an email of <user_email>
        user_list: List[User] = User.search({"email": user_email})

        if len(user_list) != 0:
            user = user_list[0]

            if not user.is_valid_password(user_pwd):
                return None

            return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance of a request.

        Arg:
            request: the request."""

        # check that request has Authorization header
        auth_value = self.authorization_header(request)
        if auth_value is None:
            return None

        # confirm that Authorization value begins with 'Basic '
        # and retrieve the substring after 'Basic '
        base64_encoded_str = self.extract_base64_authorization_header(
            auth_value)
        if base64_encoded_str is None:
            return None

        # decode the substring which is a base64 encoding
        base64_decoded_str = self.decode_base64_authorization_header(
            base64_encoded_str)
        if base64_decoded_str is None:
            return None

        # split the decoded substring into email and password
        user_credentials = self.extract_user_credentials(base64_decoded_str)
        if user_credentials == (None, None):
            return None

        # deliver the split email and password
        user = self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
        if user is None:
            return None

        return user
