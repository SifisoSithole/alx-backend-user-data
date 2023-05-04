#!/usr/bin/env python3
""" Module of Session in Database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Session in database Class
    """
    def create_session(self, user_id=None):
        """
        Make a new Session to Database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session = UserSession(
            user_id=user_id,
            session_id=session_id
        )

        if session is None:
            return None
        session.save()
        session.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Make user id to session
        """
        if session_id is None:
            return
        UserSession.load_from_file()
        user = UserSession.search({'session_id': session_id})
        if not user or len(user) == 0:
            return
        user = user[0]
        if user is None:
            return
        ex_session = user.created_at + timedelta(seconds=self.session_duration)
        if ex_session < datetime.now():
            return
        return user.user_id

    def destroy_session(self, request=None):
        """
        Destroy the auth session if this
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        user = UserSession.search({'session_id': session_id})
        if not user or user is None:
            return False
        try:
            user[0].remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
