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
            execluded_Paths (List[str]):

        Return
        ------
            (bool):
        """

        return False

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
