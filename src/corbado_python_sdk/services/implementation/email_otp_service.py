from pydantic import BaseModel, ConfigDict, StringConstraints, validate_call
from typing_extensions import Annotated

from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.exceptions.standard_exception import StandardException
from corbado_python_sdk.generated import ApiException, ErrorRsp
from corbado_python_sdk.generated.api import EmailOTPApi
from corbado_python_sdk.generated.models import (
    EmailCodeSendReq,
    EmailCodeSendRsp,
    EmailCodeValidateReq,
    EmailCodeValidateRsp,
)
from corbado_python_sdk.services import EmailOTPInterface


class EmailOTPService(BaseModel, EmailOTPInterface):
    """
    Service class for handling operations related to Email OTP (One-Time Password).

    This class provides methods to send and validate email codes using the Email OTP API.

    Attributes:
        client (EmailOTPApi): The client for Email OTP API.

    Methods:
        __init__(client: EmailOTPApi) -> None:
            Constructor for EmailOTPService.

        send(req: EmailCodeSendReq) -> EmailCodeSendRsp:
            Send email code.

        validate_email(id: str, req: EmailCodeValidateReq) -> EmailCodeValidateRsp:
            Validate email code.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: EmailOTPApi

    def send(self, req: EmailCodeSendReq) -> EmailCodeSendRsp:
        """
        Send email code.

        Args:
            req (EmailCodeSendReq): The request object for sending email code.

        Returns:
            EmailCodeSendRsp: The response object for sending email code.

        Raises:
            ServerException: If a server-side error occurs.
            StandardException: If an unexpected ErrorRsp is received.
        """

        try:
            rsp: EmailCodeSendRsp = self.client.email_code_send(email_code_send_req=req)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp

    @validate_call
    def validate_email(
        self,
        email_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)],
        req: EmailCodeValidateReq,
    ) -> EmailCodeValidateRsp:
        """
        Validate email code.

        Args:
            email_id (str): The ID of the email code.
            req (EmailCodeValidateReq): The request object for validating email code.

        Returns:
            EmailCodeValidateRsp: The response object for validating email code.

        Raises:
            ServerException: If a server-side error occurs.
            StandardException: If an unexpected ErrorRsp is received.
        """

        try:
            rsp: EmailCodeValidateRsp = self.client.email_code_validate(
                email_code_id=email_id, email_code_validate_req=req
            )
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp
