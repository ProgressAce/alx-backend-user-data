#!/usr/bin/env python3
"""Defines the authentication system."""

import bcrypt
import uuid
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

    salt: bytes = bcrypt.gensalt()
    byte_pwd: bytes = password.encode('utf-8')

    hash_pwd: str = bcrypt.hashpw(byte_pwd, salt)
    return hash_pwd


def _generate_uuid():
    """Generates and returns a string representation of a new UUID."""

    uid: uuid.UUID = uuid.uuid4()
    return str(uid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db: DB = DB()

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

        user: User
        # check if the user's email already exists
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists.')
        except (InvalidRequestError, NoResultFound):
            pass

        # add new user to the DB.
        hashed_pwd: str = _hash_password(password)

        user = self._db.add_user(email, hashed_pwd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates if login details are correct.

        Email is used to check user existence, and if confirmed
        then the password is checked.

        Args:
            email: a user's email credential.
            password: a user's password credential.

        Returns:
            True, is user exists and password is correct
            False, in all other cases."""

        if not isinstance(email, str) or len(email) < 5:
            return None
        if not isinstance(password, str) or len(email) < 1:
            return None

        try:
            user: User = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return False

        byte_pwd: bytes = password.encode('utf-8')

        if bcrypt.checkpw(byte_pwd, user.hashed_password):
            return True

        return False

    def create_session(self, email: str) -> str:
        """Creates a session ID for the user found with their email.

        Arg:
            email: email address of the user.

        Returns:
            the session ID.
        """

        if not isinstance(email, str) or len(email) < 5:
            return None

        try:
            user: User = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            return None

        session_id: str = _generate_uuid()

        self._db.update_user(user_id=user.id, session_id=session_id)
        return session_id
