#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User

VALID_ARGS = ['email', 'hashed_password', 'session_id', 'reset_token', 'id']


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
        """Maybe one day I can add users in my website"""
        if email is None or type(email) is not str:
            return None
        if hashed_password is None or type(hashed_password) is not str:
            return None
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            return None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """User finder as you can see"""
        for key, _ in kwargs.items():
            if key not in VALID_ARGS:
                raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """User updater"""
        if user_id is None or type(user_id) is not int:
            return None
        for key, _ in kwargs.items():
            if key not in VALID_ARGS:
                raise ValueError
        user = self.find_user_by(id=user_id)
        if user is None:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        return None
