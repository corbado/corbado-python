import jwt
from jwt import decode
from jwt.jwks_client import PyJWKClient
from pydantic import BaseModel, ConfigDict, StrictStr, StringConstraints
from typing_extensions import Annotated

from corbado_python_sdk.entities.session_validation_result import (
    SessionValidationResult,
)

DEFAULT_SHORT_SESSION_LENGTH = 300


class SessionService(BaseModel):
    """This class provides functionality for managing sessions.

    Including validation and retrieval of user information from short-term session tokens.

    Attributes:
        model_config (ConfigDict): Configuration dictionary for the model.
        short_session_cookie_name (str): Name of the short session cookie.
        issuer (str): Issuer of the session tokens.
        jwks_uri (str): URI of the JSON Web Key Set (JWKS) endpoint.
        last_short_session_validation_result (str): Result of the last short session validation.
        short_session_length (int): Length of short session in seconds. Default = 300
        _jwk_client (PyJWKClient): JSON Web Key (JWK) client for handling JWKS.
        cache_keys (bool): Flag to cache keys. Default = False.
        cache_jwk_set (bool): Flag to cache jwk_sets. Default = True.


    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    short_session_cookie_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    issuer: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    jwks_uri: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    last_short_session_validation_result: str = ""
    short_session_length: int = DEFAULT_SHORT_SESSION_LENGTH
    cache_keys: bool = False
    cache_jwk_set: bool = True
    _jwk_client: PyJWKClient

    def __init__(self, **kwargs) -> None:  # type: ignore
        """
        Initialize a new instance of the SessionService class.

        Args:
            **kwargs: Additional keyword arguments to initialize the SessionService.
                These keyword arguments should include values for the attributes defined in the class,
                such as 'short_session_cookie_name', 'issuer', 'jwks_uri', 'last_short_session_validation_result',
                'cache_keys',cache_jwk_set and 'short_session_length'.

        Raises:
            Any errors raised during the initialization process.

        """
        super().__init__(**kwargs)
        self._jwk_client = PyJWKClient(
            uri=self.jwks_uri,
            cache_keys=self.cache_keys,
            lifespan=self.short_session_length,
            cache_jwk_set=self.cache_jwk_set,
        )

    def get_and_validate_short_session_value(self, short_session: StrictStr) -> SessionValidationResult:
        """Validate the given short-term session (represented as JWT) value.

        Args:
            short_session (StrictStr): jwt

        Returns:
            SessionValidationResult: SessionValidationResult with authenticated=True on success,
            otherwise with authenticated=False
        """
        if not short_session:
            return SessionValidationResult(authenticated=False)
        try:
            # retrieve signing key
            signing_key: jwt.PyJWK = self._jwk_client.get_signing_key_from_jwt(token=short_session)
            # decode short session (jwt) with signing key
            payload = decode(jwt=short_session, key=signing_key.key, algorithms=["RS256"], issuer=self.issuer)

            # extract information from decoded payload
            sub = payload.get("sub")
            full_name = payload.get("name")

            return SessionValidationResult(authenticated=True, user_id=sub, full_name=full_name)
        except Exception as error:
            # return unauthenticated user on error
            self.set_validation_error(error)
            return SessionValidationResult(authenticated=False, error=error)

    def get_current_user(self, short_session: StrictStr) -> SessionValidationResult:
        """Return current user for the short session.

        Args:
            short_session (StrictStr): Short session.

        Returns:
            SessionValidationResult:  SessionValidationResult with authenticated=True on success, otherwise with
                authenticated=False.
        """
        user: SessionValidationResult = self.get_and_validate_short_session_value(short_session)
        return user

    def set_issuer_mismatch_error(self, issuer: str) -> None:
        """Set issuer mismatch error.

        Args:
            issuer (str): issuer.
        """
        self.last_short_session_validation_result = f"Mismatch in issuer (configured: {self.issuer}, JWT: {issuer})"

    def set_validation_error(self, error: Exception) -> None:
        """Set validation error.

        Args:
            error (Exception): Exception occurred.
        """
        self.last_short_session_validation_result = f"JWT validation failed: {error}"
