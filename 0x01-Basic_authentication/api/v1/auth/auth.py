#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """This is an auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Don't know yet"""
        if path is None:
            return True
        path = path.strip('/')
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for i in range(len(excluded_paths)):
            excluded_paths[i] = excluded_paths[i].strip('/')
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """What is going on here"""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """Current user thing"""
        return None
