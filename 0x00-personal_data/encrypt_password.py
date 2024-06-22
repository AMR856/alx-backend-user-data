#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """Hasher function"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validtor as you can say"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
