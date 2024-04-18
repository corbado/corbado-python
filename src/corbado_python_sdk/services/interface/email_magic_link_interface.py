from abc import ABC, abstractmethod

from pydantic import StringConstraints, validate_call
from typing_extensions import Annotated

from corbado_python_sdk.generated.models import (
    EmailLinkSendReq,
    EmailLinkSendRsp,
    EmailLinksValidateReq,
    EmailLinkValidateRsp,
)


class EmailMagicLinkInterface(ABC):
    """
    Provides methods to interact with Email Magic Links API.

    Functions:
        send: Sends an email magic link.
        validate: Validates an email magic link.
    """

    @abstractmethod
    def send(self, req: EmailLinkSendReq) -> EmailLinkSendRsp:
        """
        Sends an email magic link.

        Args:
            req (EmailLinkSendReq): The request object containing the details of the email magic link.

        Returns:
            EmailLinkSendRsp: The response object containing the result of the operation.
        """
        pass

    @abstractmethod
    @validate_call
    def validate_email_magic_link(
        self,
        email_link_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)],
        req: EmailLinksValidateReq,
    ) -> EmailLinkValidateRsp:
        """
        Validates an email magic link.

        Args:
            email_link_id (str): The ID of the email magic link to validate.
            req (EmailLinksValidateReq): The request object containing additional validation details.

        Returns:
            EmailLinkValidateRsp: The response object containing the result of the validation.
        """
        pass
