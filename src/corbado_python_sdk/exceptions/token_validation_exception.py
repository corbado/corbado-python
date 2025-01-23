from enum import Enum

from typing_extensions import Optional


class ValidationErrorType(Enum):
    """
    Enum representing types of validation errors.

    This enum categorizes various validation errors that may occur during
    token validation processes.

    Attributes:
        INVALID_TOKEN (str): Indicates that the token is invalid. More information in 'original_exception'.
        CODE_JWT_SIGNING_KEY_ERROR (str): Indicates that the signing key could not be retrieved. More information in 'original_exception'.
        CODE_JWT_CODE_JWT_EMPTY_SESSION_TOKEN (str): Indicates that the session token is empty.
        CODE_JWT_ISSUER_EMPTY (str): Indicates that the issuer is empty.
        CODE_JWT_ISSUER_MISSMATCH (str): Indicates that the token issuer does not match the expected issuer.
        CODE_JWT_BEFORE (str):Token is not yet valid.
        CODE_JWT_EXPIRED (str): Token expired.
        CODE_JWT_INVALID_SIGNATURE (str): Invalid Signature.


    """

    CODE_JWT_GENERAL = "Invalid token"  # noqa s105
    CODE_JWT_SIGNING_KEY_ERROR = "Could not retrieve signing key"
    CODE_JWT_EMPTY_SESSION_TOKEN = "Session token is empty"  # noqa s105
    CODE_JWT_ISSUER_EMPTY = "Issuer is empty"
    CODE_JWT_ISSUER_MISSMATCH = "Token issuer does not match"
    CODE_JWT_BEFORE = "Token is not yet valid"
    CODE_JWT_EXPIRED = "Token expired"
    CODE_JWT_INVALID_SIGNATURE = "Invalid Signature"


class TokenValidationException(Exception):
    """Custom exception class for handling validation errors.

    This exception wraps around other exceptions to provide additional context
    regarding validation failures.

    Attributes:
        message (str): The custom error message describing the validation error.
        error_type (ValidationErrorType): Enum value indicating the type of validation error.
        original_exception (Optional[Exception]): The original exception that caused this error, if any.
    """

    def __init__(self, message: str, error_type: ValidationErrorType, original_exception: Optional[Exception] = None):
        """Initialize ValidationError with message, error type, and optional original exception.

        Args:
            message (str): A description of the error.
            error_type (ValidationErrorType): The specific type of validation error.
            original_exception (Optional[Exception], optional): The original exception that caused
                this error, if available. Defaults to None.
        """
        super().__init__(message)
        self.message: str = message
        self.error_type: ValidationErrorType = error_type
        self.original_exception: Optional[Exception] = original_exception

    def __str__(self) -> str:
        """Return a string representation of the validation error.

        Includes the error type, custom message, and details of the original exception
        if it is available.

        Returns:
            str: Formatted string containing error type, message, and any original exception details.
        """
        base_message: str = f"[{self.error_type.value}] {self.message}"
        if self.original_exception:
            return f"{base_message} | Caused by: {repr(self.original_exception)}"
        return base_message
