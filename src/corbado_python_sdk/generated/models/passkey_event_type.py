# coding: utf-8

"""
    Corbado Backend API

     # Introduction This documentation gives an overview of all Corbado Backend API calls to implement passwordless authentication with Passkeys. 

    The version of the OpenAPI document: 2.0.0
    Contact: support@corbado.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class PasskeyEventType(str, Enum):
    """
    PasskeyEventType
    """

    """
    allowed enum values
    """
    USER_MINUS_LOGIN_MINUS_BLACKLISTED = 'user-login-blacklisted'
    LOGIN_MINUS_EXPLICIT_MINUS_ABORT = 'login-explicit-abort'
    LOGIN_MINUS_ERROR = 'login-error'
    LOGIN_MINUS_ERROR_MINUS_UNTYPED = 'login-error-untyped'
    LOGIN_MINUS_ONE_MINUS_TAP_MINUS_SWITCH = 'login-one-tap-switch'
    USER_MINUS_APPEND_MINUS_AFTER_MINUS_CROSS_MINUS_PLATFORM_MINUS_BLACKLISTED = 'user-append-after-cross-platform-blacklisted'
    USER_MINUS_APPEND_MINUS_AFTER_MINUS_LOGIN_MINUS_ERROR_MINUS_BLACKLISTED = 'user-append-after-login-error-blacklisted'
    APPEND_MINUS_CREDENTIAL_MINUS_EXISTS = 'append-credential-exists'
    APPEND_MINUS_EXPLICIT_MINUS_ABORT = 'append-explicit-abort'
    APPEND_MINUS_ERROR = 'append-error'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of PasskeyEventType from a JSON string"""
        return cls(json.loads(json_str))


