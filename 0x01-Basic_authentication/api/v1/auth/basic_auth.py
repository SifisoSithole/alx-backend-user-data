#!/usr/bin/env python3
"""
Basic Authorization module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic Authorization module
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        extracts the username and password in base64

        Arguments:
            authorization_header (str): authorixation header

        Return:
            (str): the value after Basic (after the space)
        """
        if not authorization_header or type(authorization_header) is not str:
            return None

        authorization_header = authorization_header.split()
        if authorization_header[0] != 'Basic':
            return None
        return authorization_header[1]
