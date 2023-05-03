#!/usr/bin/env python3
"""
Authorization module
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Basic Authorization class

    Methods
    -------
        require_auth:
        authorization_header:
        current_user
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        ----

        Arguments
        ---------
            path (str): path requested
            excluded_paths (List[str]): excluded paths

        Return
        ------
            (bool):
        """

        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """

        Arguments
        ---------
            request:

        Return
        -------
            (str):
        """

        if request is None:
            return None

        authorization = request.headers.get('Authorization')

        if authorization is None:
            return None

        return authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """

        Arguments
        ---------
            request:

        Return
        ------
            ():
        """
        return None

    def session_cookie(self, request=None):   
        """
        returns a cookie value from a request
        """
        if not request:
            return
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
