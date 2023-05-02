#!/usr/bin/env python3
"""
Basic Authorization module
"""
from flask import request
from typing import List, TypeVar


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
            path (str):
            excluded_paths (List[str]):

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

        if path in excluded_paths:
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
        return None

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
