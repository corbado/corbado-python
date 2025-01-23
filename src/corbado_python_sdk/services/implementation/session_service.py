import jwt
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidSignatureError,
    decode,
)
from jwt.jwks_client import PyJWKClient
from pydantic import BaseModel, ConfigDict, StrictStr, StringConstraints
from typing_extensions import Annotated

from corbado_python_sdk.entities import UserEntity, UserStatus
from corbado_python_sdk.exceptions.token_validation_exception import (
    TokenValidationException,
    ValidationErrorType,
)

DEFAULT_SESSION_TOKEN_LENGTH = 300


class SessionService(BaseModel):
    """This class provides functionality for managing sessions.

    Including validation and retrieval of user information from short-term session tokens.

    Attributes:
        model_config (ConfigDict): Configuration dictionary for the model.
        issuer (str): Issuer of the session tokens.
        jwks_uri (str): URI of the JSON Web Key Set (JWKS) endpoint.
        _jwk_client (PyJWKClient): JSON Web Key (JWK) client for handling JWKS.
        project_id (str): Corbado Project Id.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    # Fields
    issuer: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    jwks_uri: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    project_id: str
    _jwk_client: PyJWKClient

    # Constructor
    def __init__(self, **kwargs) -> None:  # type: ignore
        """
        Initialize a new instance of the SessionService class.

        Args:
            **kwargs: Additional keyword arguments to initialize the SessionService.
                These keyword arguments should include values for the attributes defined in the class,
                such as 'issuer', 'jwks_uri', 'cache_keys', 'cache_jwk_set' and 'session_token_cookie_length'.

        Raises:
            Any errors raised during the initialization process.

        """
        super().__init__(**kwargs)
        self._jwk_client = PyJWKClient(
            uri=self.jwks_uri,
            lifespan=DEFAULT_SESSION_TOKEN_LENGTH,
        )

    # Core methods
    def validate_token(self, session_token: StrictStr) -> UserEntity:
        """Validate the given short-term session (represented as JWT) value.

        Args:
            session_token (StrictStr): jwt

        Raises:
            TokenValidationException: If token is invalid.

        Returns:
            UserEntity: User Entity.
        """
        if not session_token:
            raise TokenValidationException(
                error_type=ValidationErrorType.CODE_JWT_EMPTY_SESSION_TOKEN,
                message=ValidationErrorType.CODE_JWT_EMPTY_SESSION_TOKEN.name,
            )

        # retrieve signing key
        try:
            signing_key: jwt.PyJWK = self._jwk_client.get_signing_key_from_jwt(token=session_token)
        except Exception as error:
            raise TokenValidationException(
                error_type=ValidationErrorType.CODE_JWT_SIGNING_KEY_ERROR,
                message=f"Could not retrieve signing key: {session_token}. See  original_exception for further information: {str(error)}",
                original_exception=error,
            )

        # decode short session (jwt) with signing key
        try:
            payload = decode(jwt=session_token, key=signing_key.key, algorithms=["RS256"])

            # extract information from decoded payload
            token_issuer: str = payload.get("iss")
            sub: str = payload.get("sub")
            full_name: str = payload.get("name")
        except ImmatureSignatureError as error:
            raise TokenValidationException(
                error_type=ValidationErrorType.CODE_JWT_BEFORE,
                message=f"Error occured during token decode: {session_token}. {ValidationErrorType.CODE_JWT_BEFORE.value}",
                original_exception=error,
            )
        except ExpiredSignatureError as error:
            raise TokenValidationException(
                error_type=ValidationErrorType.CODE_JWT_INVALID_SIGNATURE,
                message=f"Error occured during token decode: {session_token}. {ValidationErrorType.CODE_JWT_INVALID_SIGNATURE.value}",
                original_exception=error,
            )

        except InvalidSignatureError as error:
            raise TokenValidationException(
                error_type=ValidationErrorType.CODE_JWT_EXPIRED,
                message=f"Error occured during token decode: {session_token}. {ValidationErrorType.CODE_JWT_EXPIRED.value}",
                original_exception=error,
            )

        except Exception as error:
            raise TokenValidationException(
                error_type=ValidationErrorType.CODE_JWT_GENERAL,
                message=f"Error occured during token decode: {session_token}. See  original_exception for further information: {str(error)}",
                original_exception=error,
            )

        # validate issuer
        self._validate_issuer(token_issuer=token_issuer, session_token=session_token)
        # TODO: Retrieve user status
        return UserEntity(fullName=full_name, userID=sub, status=UserStatus.ACTIVE)

    # Private methods
    def _validate_issuer(self, token_issuer: str, session_token: str) -> None:
        """Validate issuer.

        Args:
            token_issuer (str): Token issuer.
            session_token (str): Session token.

        Raises:
            TokenValidationException: If issuer is invalid.

        """
        if not token_issuer:
            raise TokenValidationException(
                error_type=ValidationErrorType.CODE_JWT_ISSUER_EMPTY,
                message=f"Issuer is empty. Session token: {session_token}"
            )

        # Check for old Frontend API (without .cloud.)
        expected_old: StrictStr = f"https://{self.project_id}.frontendapi.corbado.io"
        if token_issuer == expected_old:
            return

        # Check for new Frontend API (with .cloud.)
        expected_new: StrictStr = f"https://{self.project_id}.frontendapi.cloud.corbado.io"
        if token_issuer == expected_new:
            return

        # Check against the configured issuer (e.g., a custom domain or CNAME)
        if token_issuer != self.issuer:
            raise TokenValidationException(
                error_type=ValidationErrorType.CODE_JWT_ISSUER_MISSMATCH,
                message=f"Issuer mismatch (configured via FrontendAPI: '{self.issuer}', JWT issuer: '{token_issuer}')",
            )
