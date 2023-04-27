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
