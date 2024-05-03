from pydantic import BaseModel, ConfigDict, StringConstraints, validate_call
from typing_extensions import Annotated

from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.exceptions.standard_exception import StandardException
from corbado_python_sdk.generated import ApiException, ErrorRsp
from corbado_python_sdk.generated.api import EmailMagicLinksApi
from corbado_python_sdk.generated.models import (
    EmailLinkSendReq,
    EmailLinkSendRsp,
    EmailLinksValidateReq,
    EmailLinkValidateRsp,
)
from corbado_python_sdk.services import EmailMagicLinkInterface


class EmailMagicLinkService(BaseModel, EmailMagicLinkInterface):
    """
    Provides methods to interact with Email Magic Links API.

    Functions:
        send: Sends an email magic link.
        validate: Validates an email magic link.

    Raises:
        ValidationError: If assertions fail.
        ServerException: If a server error occurs.
        StandardException: If an unexpected error response is received.

    Args:
        client (EmailMagicLinksApi): The client for interacting with the authentication tokens API.

    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: EmailMagicLinksApi

    def send(self, req: EmailLinkSendReq) -> EmailLinkSendRsp:
        """
        Send an email magic link.

        Args:
            req (EmailLinkSendReq): The request object containing the details of the email magic link.

        Raises:
            ServerException: If a server-side error occurs.
            StandardException: If an unexpected ErrorRsp is received.

        Returns:
            EmailLinkSendRsp: The response object containing the result of the operation.
        """
        try:
            rsp: EmailLinkSendRsp = self.client.email_link_send(email_link_send_req=req)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp

    @validate_call
    def validate_email_magic_link(
        self,
        email_link_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)],
        req: EmailLinksValidateReq,
    ) -> EmailLinkValidateRsp:
        """
        Validate an email magic link.

        Args:
            email_link_id (str): The ID of the email magic link to validate.
            req (EmailLinksValidateReq): The request object containing additional validation details.

        Returns:
            EmailLinkValidateRsp: The response object containing the result of the validation.

        Raises:
            ServerException: If a server-side error occurs.
            StandardException: If an unexpected ErrorRsp is received.

        """
        try:
            rsp: EmailLinkValidateRsp = self.client.email_link_validate(
                email_link_id=email_link_id, email_links_validate_req=req
            )
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp
