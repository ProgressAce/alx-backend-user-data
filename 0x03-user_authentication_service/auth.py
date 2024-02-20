#!/usr/bin/env python3
"""Defines the authentication system."""

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Returns a salted final hashed password in byte form.

    The input password is hashed together with a salted value
    for greater password masking.

    Arg:
        password: the password to hash."""

    if not isinstance(password, str) or len(password) < 1:
        return None

    salt = bcrypt.gensalt()
    byte_pwd = password.encode('utf-8')

    hash_pwd = bcrypt.hashpw(byte_pwd, salt)
    return hash_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Administers a new user to the database.

        Arg:
            email: the email of the new user.
            password: the user's password.

        Returns:
            the new user instance."""

        if not isinstance(email, str) or len(email) < 5:
            return None
        if not isinstance(password, str) or len(email) < 1:
            return None

        # check if the user's email already exists
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists.')
        except (InvalidRequestError, NoResultFound):
            pass

        # add new user to the DB.
        hashed_pwd = _hash_password(password)

        user = self._db.add_user(email, hashed_pwd)
        return user
