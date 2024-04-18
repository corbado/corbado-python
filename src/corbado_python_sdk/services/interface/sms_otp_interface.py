from abc import ABC, abstractmethod

from corbado_python_sdk.generated.models import (
    SmsCodeSendReq,
    SmsCodeSendRsp,
    SmsCodeValidateReq,
    SmsCodeValidateRsp,
)


class SmsOTPInterface(ABC):
    """
    Service class for sending and validating SMS codes.


    Attributes:
        client (SMSOTPApi): The client used for interacting with the SMS OTP service.

    Methods:
        send(req: SmsCodeSendReq) -> SmsCodeSendRsp:
            Sends an SMS code to a user.

        validate_sms(id: str, req: SmsCodeValidateReq) -> SmsCodeValidateRsp:
            Validates an SMS code entered by a user.
    """

    @abstractmethod
    def send(self, req: SmsCodeSendReq) -> SmsCodeSendRsp:
        """Sends an SMS code.

        Args:
            req (SmsCodeSendReq): The request object containing SMS details.

        Returns:
            SmsCodeSendRsp: The response object containing the result of the operation.
        """
        pass

    @abstractmethod
    def validate_sms(self, sms_id: str, req: SmsCodeValidateReq) -> SmsCodeValidateRsp:
        """Validates an SMS code.

        Args:
            sms_id (str): The ID of the SMS code to validate.
            req (SmsCodeValidateReq): The request object containing SMS validation details.

        Returns:
            SmsCodeValidateRsp: The response object containing the result of the validation.
        """
        pass
