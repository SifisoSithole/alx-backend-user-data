#!/usr/bin/env python3
"""
This module is used to Encryp a password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Uses the bcrypt package to perform the hashing (with hashpw)

    Arguments:
        password (str): User password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Uses the bcrypt package to validate password

    Arguments:
        hashed_password (bytes): hashed password
        password (str): User password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
