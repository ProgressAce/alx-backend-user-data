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


def _generate_uuid() -> str:
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
        except NoResultFound:
            pass
        except InvalidRequestError:
            return None

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

    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets the user of the related session ID.

        Arg:
            session_id: the session ID belonging to a specific user.

        Returns:
            None - if the user is not found or session ID is None.
            user instnace - if the user was found.
        """

        if not session_id:
            return None

        try:
            user: User = self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates a user's session ID to None.

        This indicates that the user's session ID has been discarded.

        Arg:
            session_id: the session ID to discard.
        """

        if not isinstance(user_id, int):
            raise ValueError

        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError as err:
            raise err

        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset token for a specific user.

        The user is found via the <email> provided.
        A reset token is generated for the user in the form of a UUID.

        Raises:
          - ValueError, if user does not exist.

        Returns:
          - the reset token, a UUID, if the user exists.
        """

        if not isinstance(email, str) or len(email) < 5:
            raise ValueError

        # InvalidRequestError does not need to be handled yet
        try:
            user: User = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token: uuid.UUID = uuid.uuid4()

        # raises ValueError for arguments not corresponding to the user model
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the hashed password of the specified user.

        The reset_token is used to find the specific user.
        The password is hashed and updates the user's current passsword
        with this new one.

        Args:
            reset_token: token used to find the specific user.
            password: the password replace the user's existing one.

        Raises:
          - ValueError, if the user does not exist.
        """

        if not isinstance(reset_token, str) or len(reset_token) < 1:
            raise ValueError

        if not isinstance(password, str) or len(password) < 1:
            raise ValueError

        # InvalidRequestError does not need to be handled yet
        try:
            user: User = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_pwd: str = _hash_password(password)

        # raises ValueError for arguments not corresponding to the user model
        self._db.update_user(user.id, hashed_password=hashed_pwd)
        self._db.update_user(user.id, reset_token=None)
