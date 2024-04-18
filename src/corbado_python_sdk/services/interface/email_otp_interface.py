from abc import ABC, abstractmethod

from pydantic import Field, StringConstraints
from typing_extensions import Annotated

from corbado_python_sdk.generated.models import (
    EmailCodeSendReq,
    EmailCodeSendRsp,
    EmailCodeValidateReq,
    EmailCodeValidateRsp,
)


class EmailOTPInterface(ABC):
    """
    Service class for handling operations related to Email OTP (One-Time Password).

    This class provides methods to send and validate email codes using the Email OTP API.

    Attributes:
        client (EmailOTPApi): The client for Email OTP API.

    Methods:
        send(req: EmailCodeSendReq) -> EmailCodeSendRsp:
            Send email code.

        validate_email(id: str, req: EmailCodeValidateReq) -> EmailCodeValidateRsp:
            Validate email code.

    """

    @abstractmethod
    def send(self, req: EmailCodeSendReq) -> EmailCodeSendRsp:
        """
        Send email code.

        Args:
            req (EmailCodeSendReq): The request object for sending email code.

        Returns:
            EmailCodeSendRsp: The response object for sending email code.

        """

        pass

    @abstractmethod
    def validate_email(
        self,
        email_id: Annotated[str, Field(StringConstraints(strip_whitespace=True, min_length=1))],
        req: EmailCodeValidateReq,
    ) -> EmailCodeValidateRsp:
        """
        Validate email code.

        Args:
            email_id (str): The ID of the email code.
            req (EmailCodeValidateReq): The request object for validating email code.

        Returns:
            EmailCodeValidateRsp: The response object for validating email code.

        """
