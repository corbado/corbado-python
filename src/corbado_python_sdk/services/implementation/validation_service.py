from pydantic import BaseModel, ConfigDict

from corbado_python_sdk.exceptions.server_exception import ServerException
from corbado_python_sdk.exceptions.standard_exception import StandardException
from corbado_python_sdk.generated import ErrorRsp
from corbado_python_sdk.generated.api import ValidationApi
from corbado_python_sdk.generated.exceptions import ApiException
from corbado_python_sdk.generated.models import (
    ValidateEmailReq,
    ValidateEmailRsp,
    ValidatePhoneNumberReq,
    ValidatePhoneNumberRsp,
)
from corbado_python_sdk.services.interface import ValidationInterface


class ValidationService(
    BaseModel,
    ValidationInterface,
):
    """Service for validation functionality."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: ValidationApi

    def validate_email(self, req: ValidateEmailReq) -> ValidateEmailRsp:
        """
        Validates an email address.

        Args:
            req (ValidateEmailReq): The request object for email validation.

        Raises:
            ServerException: If any server-side error occurs.
            StandardException: If an unexpected ErrorRsp is received.

        Returns:
            ValidateEmailRsp: The response object.
        """
        try:
            rsp: ValidateEmailRsp = self.client.validate_email(req)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp

    def validate_phone_number(self, req: ValidatePhoneNumberReq) -> ValidatePhoneNumberRsp:
        """
        Validates a phone number.

        Args:
            req (ValidatePhoneNumberReq): The request object for phone number validation.

        Raises:
            ServerException: If any server-side error occurs.
            StandardException: If an unexpected ErrorRsp is received.

        Returns:
            ValidatePhoneNumberRsp: The response object.
        """
        try:
            rsp: ValidatePhoneNumberRsp = self.client.validate_phone_number(req)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp
