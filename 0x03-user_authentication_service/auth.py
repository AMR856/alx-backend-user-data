#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Optional


def _generate_uuid() -> str:
    """The best generator in the world"""
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Password encryptor"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validtor as you can say"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validator thing"""
        try:
            user = self._db.find_user_by(email=email)
            string_repr = user.hashed_password
            stripped_string = string_repr.strip("b'")
            bytes_object = stripped_string.encode('utf-8')
            return bcrypt.checkpw(
                    password.encode("utf-8"),
                    bytes_object,
                )
        except NoResultFound as error:
            return False

    def create_session(self, email: str) -> str:
        """Session creatro"""
        try:
            user = self._db.find_user_by(email=email)
            uuid_id = _generate_uuid()
            self._db.update_user(user.id, session_id=uuid_id)
            return uuid_id
        except NoResultFound as error:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """User getter from session id"""
        if session_id is None or type(session_id) is not str:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound as error:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Session destroyer"""
        if user_id is None or type(user_id) is not int:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound as error:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """token reseter thing"""
        try:
            user = self._db.find_user_by(email=email)
            uuid_id = _generate_uuid()
            self._db.update_user(user.id, reset_token=uuid_id)
            return uuid_id
        except NoResultFound as error:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Password updater"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password_bytes = _hash_password(password)
            self._db.update_user(user.id, hashed_password=password_bytes)
            self._db.update_user(user.id, reset_token=None)
            return None
        except NoResultFound as error:
            raise ValueError
