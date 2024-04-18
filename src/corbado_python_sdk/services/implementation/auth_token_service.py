from pydantic import BaseModel, ConfigDict

from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.exceptions.standard_exception import StandardException
from corbado_python_sdk.generated import ApiException, ErrorRsp
from corbado_python_sdk.generated.api import AuthTokensApi
from corbado_python_sdk.generated.models import (
    AuthTokenValidateReq,
    AuthTokenValidateRsp,
)
from corbado_python_sdk.services import AuthTokenInterface


class AuthTokenService(BaseModel, AuthTokenInterface):
    """
    Service class for handling authentication tokens.

    This class provides methods to interact with authentication tokens
    using the provided client.

    Functions:
        validate(req: AuthTokenValidateReq) -> AuthTokenValidateRsp:
            Validate an authentication token.

    Args:
        client (AuthTokensApi): The client for interacting with the authentication tokens API.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    client: AuthTokensApi

    def validate_auth_token(self, req: AuthTokenValidateReq) -> AuthTokenValidateRsp:
        """
        Validate an authentication token.

        Args:
            req (AuthTokenValidateReq): The request object containing the authentication token to validate.

        Returns:
            AuthTokenValidateRsp: The response object containing the validation result.

        Raises:
            StandardException: If an unexpected error response is received.
            ServerException: If an error occurs while validating the authentication token.
        """
        try:
            rsp: AuthTokenValidateRsp = self.client.auth_token_validate(auth_token_validate_req=req)
        except ApiException as e:
            raise ServerException(e)

        if isinstance(rsp, ErrorRsp):
            raise StandardException("Got unexpected ErrorRsp")

        return rsp
