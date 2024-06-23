#!/usr/bin/env python3
""" Module of session Auth
"""

from api.v1.auth.auth import Auth
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
