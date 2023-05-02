#!/usr/bin/env python3
"""
Basic Authorization module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from codecs import decode
from models.user import User
from typing import TypeVar


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

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if not user_email or type(user_email) is not str:
            return

        if not user_pwd or type(user_pwd) is not str:
            return

        users = User()
        user = users.search({'email': user_email})
        if type(user) is not list or len(user) == 0:
            return
        user = user[0]
        if not user.is_valid_password(user_pwd):
            return
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieves the User instance for a request
        """
        authorization_header = self.authorization_header(request)
        header = self.extract_base64_authorization_header(authorization_header)
        decoded = self.decode_base64_authorization_header(header)
        email, password = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(email, password)
