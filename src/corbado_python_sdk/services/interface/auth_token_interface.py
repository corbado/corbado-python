from abc import ABC, abstractmethod

from corbado_python_sdk.generated.models import (
    AuthTokenValidateReq,
    AuthTokenValidateRsp,
)


class AuthTokenInterface(ABC):
    """
    Interface for handling authentication tokens.
    """

    @abstractmethod
    def validate_auth_token(self, req: AuthTokenValidateReq) -> AuthTokenValidateRsp:
        """
        Validate an authentication token.

        Args:
            req (AuthTokenValidateReq): The request object containing the authentication token to validate.

        Returns:
            AuthTokenValidateRsp: The response object containing the validation result.

        """
        pass
