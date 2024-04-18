from pydantic import BaseModel, ConfigDict

from corbado_python_sdk.exceptions.server_exception import ServerException
from corbado_python_sdk.exceptions.standard_exception import StandardException
from corbado_python_sdk.generated import ErrorRsp
from corbado_python_sdk.generated.api import SMSOTPApi
from corbado_python_sdk.generated.exceptions import ApiException
from corbado_python_sdk.generated.models import (
    SmsCodeSendReq,
    SmsCodeSendRsp,
    SmsCodeValidateReq,
    SmsCodeValidateRsp,
)
from corbado_python_sdk.services.interface import SmsOTPInterface


class SmsOTPService(BaseModel, SmsOTPInterface):
    """
    Service class for sending and validating SMS codes.


    Attributes:
        client (SMSOTPApi): The client used for interacting with the SMS OTP service.

    Methods:
        send(req: SmsCodeSendReq) -> SmsCodeSendRsp:
            Sends an SMS code to a user.

        validate_sms(id: str, req: SmsCodeValidateReq) -> SmsCodeValidateRsp:
            Validates an SMS code entered by a user.

    Raises:
        ServerException: If a server-side error occurs.
        StandardException: If an unexpected error response is received.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: SMSOTPApi

    def send(self, req: SmsCodeSendReq) -> SmsCodeSendRsp:
        """
        Sends an SMS code to a user.

        Args:
            req (SmsCodeSendReq): The request containing information for sending the SMS code.

        Returns:
            SmsCodeSendRsp: The response containing information about the sent SMS code.

        Raises:
            ServerException: If a server-side error occurs.
            StandardException: If an unexpected error response is received.
        """
        try:
            rsp: SmsCodeSendRsp = self.client.sms_code_send(sms_code_send_req=req)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp

    def validate_sms(self, sms_id: str, req: SmsCodeValidateReq) -> SmsCodeValidateRsp:
        """
        Validates an SMS code entered by a user.

        Args:
            sms_id (str): The identifier associated with the SMS code.
            req (SmsCodeValidateReq): The request containing the SMS code to validate.

        Returns:
            SmsCodeValidateRsp: The response containing information about the validation result.

        Raises:
            ServerException: If a server-side error occurs.
            StandardException: If an unexpected error response is received.
        """
        try:
            rsp: SmsCodeValidateRsp = self.client.sms_code_validate(sms_code_id=sms_id, sms_code_validate_req=req)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp
