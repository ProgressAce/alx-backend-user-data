#!/usr/bin/env python3
"""
Main file
"""
from bcrypt import gensalt, hashpw, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password.

    Returns:
      - bytes, which is a salted hash of the given password.
    """
    if not isinstance(password, str):
        raise TypeError('`password` should be a string')

    try:
        # converted to bytes in order to hash
        b_password = password.encode('utf-8')

        salt = gensalt()
        hashed_password: bytes = hashpw(b_password, salt)

    except UnicodeEncodeError:
        raise UnicodeEncodeError

    return hashed_password


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID.
    """
    u_id = str(uuid4())
    return u_id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Saves a new user to the database.

        Dependency:
          - This module's `_hash_password` is used to hash the password before
          storing it in the database.

        Raises:
          - ValueError: if a user with the same email already exists.
        Returns:
          - The registered user.
        """
        if not isinstance(email, str):
            raise TypeError('<email> should be a string')
        if not isinstance(password, str):
            raise TypeError('<password> should be a string')

        if not email:
            raise ValueError('<email> should not be empty')
        if not password:
            raise ValueError('<password> should not be empty')

        try:
            user = self._db.find_user_by(email=email)

            # an exception is raised since user already exists with this email
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password: bytes = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks the authenticity of a user's login details.

        The user is located via their email, and their password is then
        checked with bcrypt.
        Returns:
          - True if all the credentials of the user is correct
          - False if the credentials are incorrect.
        """
        if not email or not password:
            return False

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        if not checkpw(password.encode('utf-8'), user.hashed_password):
            return False

        return True

    def create_session(self, email: str) -> str:
        """Provides a session ID as a string.

        Finds an user with their email. Generates a uuid and stores it in the
        database as the user's session id.

        Returns:
          - the generated session id for the user.
        """
        if not email:
            return None

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id: str = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns an user associated with the given session id.

        Returns:
          - the User corresponding to the session id.
          - otherwise None.
        """
        if not session_id:
            return None

        try:
            user: User = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: str) -> None:
        """Deletes a user's session_id.

        The session_id belonging to the user in the database is set to None
        and saved.

        Fault:
          - no exception is raised for an incorrect argument or unsuccessful
          operation of the function. COULD raise ValueError in place of None!
        """
        if not user_id:
            return None

        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

        return None

    def get_reset_password_token(self, email: str) -> str:
        """Provides a reset password token.

        Finds the user with the given email.
        If the user exists, it generates a UUID and updates the user’s
        reset_token database field.

        Exception:
          - ValueError: If the user does not exist.
        Returns:
          - the reset password token.
        """
        if not email:
            return None

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError('The user does not exist')

        reset_pwd_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_pwd_token)

        return reset_pwd_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password of an user.

        Should the reset token's association to the user be valid, then
        the new password will be hashed and the reseet token will be set
        to None. These changes will be made to the database.

        Exception:
          - ValueError: if invalid args ar provided or,
          if the user does not exist.
        """
        if not reset_token or not password:
            raise ValueError

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
