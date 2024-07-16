#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password) -> User:
        """Saves a new user to the database.
        No validation is done.
        Returns:
          - The new user.        
        """
        user: User = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Looks for users in the database that match the requirements.
        No validation of input arguments are done yet.

        Only the FIRST user is returned. The kwargs are used as the filter
        criteria.
        Raises:
          - InvalidRequestError: when any keyworded argument is invalid
          (not an attribute of user).
          - NoResultFound: when a user is not found with the database query.
        Returns:
          - the first record of the matched query for the user table.
        """
        valid_keys = ['id', 'email', 'hashed_password',
                      'session_id', 'reset_token']

        for key in kwargs.keys():
            if key not in valid_keys:
                raise InvalidRequestError

        user: User = self._session.query(User).filter_by(**kwargs).first()

        if not user:
            raise NoResultFound

        return user
