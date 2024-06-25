#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Password encryptor"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """User register"""
        if email is None or type(email) is not str:
            return None
        if password is None or type(password) is not str:
            return None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(f"{email} already exists")
        except NoResultFound as error:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=str(hashed_password))
            return user
