from abc import ABC, abstractmethod

from corbado_python_sdk.generated.models import (
    ValidateEmailReq,
    ValidateEmailRsp,
    ValidatePhoneNumberReq,
    ValidatePhoneNumberRsp,
)


class ValidationInterface(ABC):
    """Interface for validation functionality."""

    @abstractmethod
    def validate_email(self, req: ValidateEmailReq) -> ValidateEmailRsp:
        """
        Validate an email address.

        Args:
            req (ValidateEmailReq): The request object for email validation.

        Returns:
            ValidateEmailRsp: The response object.
        """
        pass

    @abstractmethod
    def validate_phone_number(self, req: ValidatePhoneNumberReq) -> ValidatePhoneNumberRsp:
        """Validate a phone number.

        Args:
            req (ValidatePhoneNumberReq): The request object for phone number validation.

        Returns:
            ValidatePhoneNumberRsp: The response object.
        """
        pass
