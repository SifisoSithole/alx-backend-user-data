#!/usr/bin/env python3
"""
Session Authentication module
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    Session Authentication
    """

    def __init__(self):
        """
        initialize class
        """
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for `user_id`
        """
        if not user_id or type(user_id) is not str:
            return
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
