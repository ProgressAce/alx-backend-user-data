#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from typing import Dict
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves a new user to the database.

        Args:
            email: the email of the new user.
            hashed_password: the password of the new user.

            Returns:
                the new user object."""

        # TODO: validation of args
        user: User = User(email=email, hashed_password=hashed_password)

        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: Dict) -> User:
        """Looks for a user/row in the 'users' database table.

        Args:
            kwargs: keyworded arguments indicating which attribute values
            to update for the user."""

        # TODO: validate args
        try:
            user: User = self._session.query(User).filter_by(**kwargs).one()
        except (NoResultFound, InvalidRequestError) as exception:
            raise exception
        return user

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """Updates a user's details in the DB.

        Arg:
            user_id: ID to identify the user.
            kwargs: keyworded arguments indicating which attribute values
            to update for the user."""

        if not isinstance(user_id, int) or user_id < 1:
            return -1

        # no error catching used
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError

        self._session.add(user)
        self._session.commit()

        return None
