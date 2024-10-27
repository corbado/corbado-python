from enum import Enum

from typing_extensions import Optional


class ValidationErrorType(Enum):
    """
    Enum representing types of validation errors.

    Attributes:
        MISSING_FIELD (str): Indicates a required field is missing.
        INVALID_FORMAT (str): Indicates an incorrect format in the data.
        VALUE_OUT_OF_RANGE (str): Indicates a value is outside the acceptable range.
        UNAUTHORIZED_ACCESS (str): Indicates unauthorized access attempt.
    """

    INVALID_TOKEN = "Invalid token"  # noqa s105
    SIGNING_KEY_ERROR = "Could not retrieve signing key"
    EMPTY_SESSION_TOKEN = "Session token is empty"  # noqa s105
    EMPTY_ISSUER = "Issuer is empty"
    ISSUER_MISSMATCH = "Token issuer does not match"


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
        self.original_exception: Exception | None = original_exception

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
