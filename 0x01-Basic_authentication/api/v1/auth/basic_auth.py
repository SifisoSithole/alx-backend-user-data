#!/usr/bin/env python3
"""
Basic Authorization module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from codecs import decode


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        decode base64 string to as a UTF8 string
        """
        if not base64_authorization_header:
            return

        if type(base64_authorization_header) is not str:
            return

        try:
            decoded_bytes = b64decode(base64_authorization_header)
            return decode(decoded_bytes, 'utf-8')
        except Exception:
            return

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if type(decoded_base64_authorization_header) is not str:
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(':')
        return credentials[0], credentials[1]
