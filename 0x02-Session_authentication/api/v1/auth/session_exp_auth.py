#!/usr/bin/env python3
"""
Session Authentication module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session Authentication module
    """

    def __init__(self):
        """
        initialize class
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except TypeError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID for `user_id`
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return
        session = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns a User ID based on a Session ID
        """
        if not session_id:
            return
        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return
        if self.session_duration <= 0:
            return session['user_id']
        created_at = session.get('created_at')
        if not created_at:
            return
        expired_session = created_at + timedelta(seconds=self.session_duration)
        if expired_session < datetime.now():
            return
        return session['user_id']
