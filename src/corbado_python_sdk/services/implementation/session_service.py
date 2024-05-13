import jwt
from jwt import decode
from jwt.exceptions import PyJWTError
from jwt.jwks_client import PyJWKClient
from pydantic import BaseModel, ConfigDict, StringConstraints
from typing_extensions import Annotated

from corbado_python_sdk.entities.user_entity import UserEntity
from corbado_python_sdk.services.interface import SessionInterface

DEFAULT_SHORT_SESSION_LENGTH = 300


class SessionService(SessionInterface, BaseModel):
    """
    Implementation of SessionInterface.

    This class provides functionality for managing sessions, including validation and retrieval of user information
    from short-term session tokens.

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

    def get_and_validate_short_session_value(self, short_session: str) -> UserEntity:
        """Validate the given short-term session (represented as JWT) value.

        Args:
            short_session (str): jwt

        Returns:
            UserEntity: UserEntity with authenticated=True on success, otherwise with authenticated=False
        """
        if not short_session:
            return UserEntity(authenticated=False)
        try:
            # retrieve signing key
            signing_key: jwt.PyJWK = self._jwk_client.get_signing_key_from_jwt(token=short_session)
            # decode short session (jwt) with signing key
            payload = decode(jwt=short_session, key=signing_key.key, algorithms=["RS256"])

            # extract information from decoded payload
            sub = payload.get("sub")
            name = payload.get("name")
            email = payload.get("email")
            phone_number = payload.get("phone_number")

            # check issuer
            if payload.get("iss") and payload["iss"] != self.issuer:
                self.set_issuer_mismatch_error(issuer=payload["iss"])
                # return unauthenticated user on issuer mismatch
                return UserEntity(authenticated=False)
            return UserEntity.create_authenticated_user(phone_number=phone_number, email=email, name=name, user_id=sub)
        except PyJWTError as error:
            # return unauthenticated user on error
            self.set_validation_error(error)
            return UserEntity(authenticated=False)

    def get_current_user(self, short_session: str) -> UserEntity:
        """Return current user for the short session.

        Args:
            short_session (str): Short session.

        Returns:
            UserEntity:  UserEntity with authenticated=True on success, otherwise with authenticated=False.
        """
        if not short_session:
            return UserEntity(authenticated=False)

        user: UserEntity = self.get_and_validate_short_session_value(short_session)
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
