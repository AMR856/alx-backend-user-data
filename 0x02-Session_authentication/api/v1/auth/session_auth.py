#!/usr/bin/env python3
""" Module of session Auth
"""

from api.v1.auth.auth import Auth
from models.user import User
# import logging
import os
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """Here I'm starting to get angry ain't gonna lie"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Session creator"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Getter for user from session"""
        if session_id is None or type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """This function can make problems as you can see"""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user
