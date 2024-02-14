#!/usr/bin/env python3
"""Implements a Basic Authentication system."""

import base64
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
        except:
            return None

        return decoded_base64.decode("utf-8")
