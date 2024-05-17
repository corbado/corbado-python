import base64
import json
import platform
from importlib.metadata import version

from pydantic import BaseModel, ConfigDict, StringConstraints, validate_call
from typing_extensions import Annotated, Dict, Optional

from corbado_python_sdk import Config
from corbado_python_sdk.generated.api import (
    AuthTokensApi,
    EmailMagicLinksApi,
    EmailOTPApi,
    SMSOTPApi,
    UserApi,
    ValidationApi,
)
from corbado_python_sdk.generated.api_client import ApiClient
from corbado_python_sdk.generated.configuration import Configuration
from corbado_python_sdk.generated.models.client_info import ClientInfo
from corbado_python_sdk.services.implementation import (
    AuthTokenService as AuthTokenService,
)
from corbado_python_sdk.services.implementation import (
    EmailMagicLinkService,
    EmailOTPService,
    SessionService,
    SmsOTPService,
    UserService,
    ValidationService,
)
from corbado_python_sdk.services.interface import (
    AuthTokenInterface,
    EmailMagicLinkInterface,
    EmailOTPInterface,
    SessionInterface,
    SmsOTPInterface,
    UserInterface,
    ValidationInterface,
)

CORBADO_HEADER_NAME = "X-Corbado-SDK"


class CorbadoSDK(BaseModel):
    """Entry point for the SDK."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    config: Config
    _api_client: Optional[ApiClient] = None
    _sessions: Optional[SessionService] = None
    _users: Optional[UserInterface] = None
    _validations: Optional[ValidationInterface] = None
    _sms_otps: Optional[SmsOTPInterface] = None
    _email_otps: Optional[EmailOTPInterface] = None
    _email_magic_links: Optional[EmailMagicLinkInterface] = None
    _auth_tokens: Optional[AuthTokenInterface] = None

    @property
    def api_client(self) -> ApiClient:
        """Get ApiClient.

        Returns:
            ApiClient: ApiClient object.
        """
        if not self._api_client:
            self._api_client = ApiClient(configuration=self._create_generated_configuration())
            python_version: str = platform.python_version()
            data: Dict[str, str] = {
                "name": "Python SDK",
                "sdkVersion": version(distribution_name="corbado-python"),
                "languageVersion": python_version,
            }
            self._api_client.set_default_header(  # type: ignore
                header_name=CORBADO_HEADER_NAME, header_value=json.dumps(data)
            )
        return self._api_client

    # --------- Interfaces ---------------#
    @property
    def email_magic_links(self) -> EmailMagicLinkInterface:
        """Get user EmailMagicLinkInterface.

        Returns:
            EmailMagicLinkInterface: EmailMagicLinkInterface object.
        """
        if not self._email_magic_links:
            self._email_magic_links = EmailMagicLinkService(client=EmailMagicLinksApi(api_client=self.api_client))
        return self._email_magic_links

    @property
    def sessions(self) -> SessionInterface:
        """Get user SessionInterface.

        Returns:
            SessionInterface: SessionInterface object.
        """
        if not self._sessions:
            self._sessions = SessionService(
                short_session_cookie_name=self.config.short_session_cookie_name,
                issuer=self.config.issuer,
                jwks_uri=self.config.frontend_api + "/.well-known/jwks",
            )

        return self._sessions

    @property
    def auth_tokens(self) -> AuthTokenInterface:
        """Get user AuthTokenInterface.

        Returns:
            AuthTokenInterface: AuthTokenInterface object.
        """
        if not self._auth_tokens:
            self._auth_tokens = AuthTokenService(client=AuthTokensApi(api_client=self.api_client))
        return self._auth_tokens

    @property
    def users(self) -> UserInterface:
        """Get user interface.

        Returns:
            UserInterface: UserInterface object.
        """
        if not self._users:
            self._users = UserService(client=UserApi(api_client=self.api_client))

        return self._users

    @property
    def email_otps(self) -> EmailOTPInterface:
        """Get E-mail OTP interface.

        Returns:
            EmailOTPInterface: EmailOTPInterface object.
        """
        if not self._email_otps:
            self._email_otps = EmailOTPService(client=EmailOTPApi(api_client=self.api_client))
        return self._email_otps

    @property
    def sms_otps(self) -> SmsOTPInterface:
        """Get SMS OTP interface.

        Returns:
            SmsOTPInterface: SmsOTPInterface object.
        """
        if not self._sms_otps:
            self._sms_otps = SmsOTPService(client=SMSOTPApi(api_client=self.api_client))
        return self._sms_otps

    @property
    def validations(self) -> ValidationInterface:
        """Get validation interface.

        Returns:
            ValidationInterface: ValidationInterface object.
        """
        if not self._validations:
            self._validations = ValidationService(client=ValidationApi(api_client=self.api_client))
        return self._validations

    # ----------- Functions ----------#
    @validate_call
    def create_client_info(
        self,
        remote_address: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)],
        user_agent: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)],
    ) -> ClientInfo:
        """Create client info.

        Args:
            remote_address (Annotated[str, Field, optional): Defaults to 1, strict=True)] remote address.
            user_agent (Annotated[str, Field, optional): Defaults to 1)] user agent.

        Returns:
            ClientInfo: ClientInfo object.
        """
        client: ClientInfo = ClientInfo(remoteAddress=remote_address, userAgent=user_agent)
        return client

    def _create_generated_configuration(self) -> Configuration:
        """Create configuration (generated class).

        Returns:
            Configuration: Configuration object.
        """
        return Configuration(
            host=self.config.backend_api,
            username=self.config.project_id,
            password=self.config.api_secret,
            access_token=None,
            api_key={"projectID": self.config.project_id},
        )

    def _generate_basic_auth_header(self, username: str, password: str) -> str:
        """Generate basic auth header.

        Args:
            username (str): ProjectId
            password (str): API Secret

        Returns:
            str: base64 encoded header value for basic authentication
        """
        credentials: str = f"{username}:{password}"
        encoded_credentials: str = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
