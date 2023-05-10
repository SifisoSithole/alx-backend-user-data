#!/usr/bin/env python3
"""
Password Hashing
"""
import bcrypt


def _hash_password(password: str) -> str:
    """
    returnes bytes salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
