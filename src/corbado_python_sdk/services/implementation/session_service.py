import jwt
from jwt import decode
from jwt.exceptions import PyJWTError
from pydantic import BaseModel, ConfigDict, StringConstraints
from typing_extensions import Annotated

SHORT_SESSION_LENGTH = 300

from jwt.jwks_client import PyJWKClient

from corbado_python_sdk.entities import UserEntity
from corbado_python_sdk.generated.api_client import ApiClient
from corbado_python_sdk.services import SessionInterface

# from requests_cache import CacheItemPoolInterface


class SessionService(BaseModel, SessionInterface):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    api_client: ApiClient = ApiClient()
    short_session_cookie_name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    issuer: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    jwks_uri: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    _jwk_client: PyJWKClient  # PyJWKClient(uri=jwks_uri, cache_keys=True,headers={"X-Corbado-ProjectID": self.})
    last_short_session_validation_result: str = ""

    @property
    def jwk_client(self) -> PyJWKClient:
        """Get PyJWKClient

        Returns:
            PyJWKClient: PyJWKClient object.
        """
        if not self._jwk_client:
            self._jwk_client = PyJWKClient(
                uri=self.jwks_uri, cache_keys=True, headers={"X-Corbado-ProjectID": self.api_client.configuration.username}  # type: ignore
            )
        return self._jwk_client

    def extract_bearer_token(self, authorization_header: str) -> str:
        if not authorization_header.startswith("Bearer "):
            return ""

        return authorization_header[7:]

    # def get_short_session_value(self) -> str:
    #   if self.short_session_cookie_name in os.environ:
    #       return os.environ[self.short_session_cookie_name]

    #   authorization_header = os.environ.get("HTTP_AUTHORIZATION", "")
    #   if authorization_header:
    #      return self.extract_bearer_token(authorization_header)

    def validate_short_session_value(self, short_session: str) -> UserEntity:
        if not short_session:
            return UserEntity(authenticated=False)

        try:
            signing_key: jwt.PyJWK = self.jwk_client.get_signing_key_from_jwt(token=short_session)
            payload = decode(short_session, signing_key.key, issuer=self.issuer, algorithms=["RS256"])

            self.jwk_client.fetch_data()

            sub = payload.get("sub")
            name = payload.get("name")
            email = payload.get("email")
            phone_number = payload.get("phoneNumber")

            if payload.get("iss") and payload["iss"] != self.issuer:
                self.set_issuer_mismatch_error(payload["iss"])
                return UserEntity(authenticated=False)

            return UserEntity.create_authenticated_user(phone_number=phone_number, email=email, name=name, user_id=sub)
        except PyJWTError as error:
            self.set_validation_error(error)
            return UserEntity(authenticated=False)

    def get_current_user(self, short_session: str) -> UserEntity:
        if not short_session:  # or len(short_session) < MIN_SHORT_SESSION_LENGTH:
            return UserEntity(authenticated=False)

        user: UserEntity = self.validate_short_session_value(short_session)
        return user

    def set_issuer_mismatch_error(self, issuer: str) -> None:
        self.last_short_session_validation_result = f"Mismatch in issuer (configured: {self.issuer}, JWT: {issuer})"

    def set_validation_error(self, error: Exception) -> None:
        self.last_short_session_validation_result = f"JWT validation failed: {error}"
