#!/usr/bin/env python3
"""
Password Hashing
"""
import bcrypt
from db import DB, User
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """
        Register a new user
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            password = _hash_password(password)
            return self._db.add_user(email, password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates login
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        find the user corresponding to the email, generate a new UUID
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """
        retreives a user using a session id
        """
        if not session_id:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return

    def destroy_session(self, user_id: int):
        """
        destroyes a session
        """
        if type(user_id) is not int:
            return
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return

    def get_reset_password_token(self, email: str) -> str:
        """
        resets password and returns a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        generated_id = _generate_uuid()
        self._db.update_user(user.id, reset_token=generated_id)
        return generated_id

    def update_password(self, reset_token: str, password: str):
        """
        updates user password based reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed_password = _hash_password(password)
        try:
            self.db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except Exception:
            raise ValueError


def _hash_password(password: str) -> str:
    """
    returnes bytes salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a string representation of a new UUID
    """
    return str(uuid.uuid4())
