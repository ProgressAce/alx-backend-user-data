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

