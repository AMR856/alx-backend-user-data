#!/usr/bin/env python3
""" Module of basicAuth
"""
import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
# import logging

# logger = logging.getLogger()
# logging.basicConfig(filename='logger.log')


class BasicAuth(Auth):
    """"Do you think we'll see the space one day"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """I got you the extractor"""
        if authorization_header is None or \
                type(authorization_header) is not str:
            return None
        authorization_header_list = authorization_header.split(' ')
        if authorization_header_list[0] != 'Basic':
            return None
        return authorization_header_list[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> str:
        """I got you the decoder"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_value_bytes = base64.b64decode(base64_authorization_header)
            decoded_value = decoded_value_bytes.decode('utf-8')
            return decoded_value
        except Exception as Anything:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) \
            -> Tuple[str, str]:
        """Do you think this is so important?"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        the_values_list = decoded_base64_authorization_header.split(':')
        return tuple(the_values_list)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> \
            TypeVar('User'):  # type: ignore
        """Do you think this is so important?"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        if User.count() == 0:
            return None
        my_user_list = User.search({'email': user_email})
        if len(my_user_list) == 0:
            return None
        for elm in my_user_list:
            if User.is_valid_password(elm, user_pwd) is False:
                continue
            return elm
        return None
