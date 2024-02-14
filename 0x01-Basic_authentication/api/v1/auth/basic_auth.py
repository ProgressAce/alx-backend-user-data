#!/usr/bin/env python3
"""Implements a Basic Authentication system."""

import base64
import binascii
from api.v1.auth.auth import Auth


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
        except binascii.Error:
            return None

        return decoded_base64.decode("utf-8")

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value.

        It is assumed that <decoded_base64_authorization_header> will
        only contain one ':'.

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
        split_str = decoded_base64_authorization_header.split(':')

        return (split_str[0], split_str[1])
