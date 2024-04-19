import base64
import json
import platform

from pydantic import BaseModel, ConfigDict, StringConstraints, validate_call
from typing_extensions import Annotated, Optional

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
    AuthTokenService,
    EmailMagicLinkService,
    EmailOTPService,
    SmsOTPService,
    UserService,
    ValidationService,
)
from corbado_python_sdk.services.interface import (
    AuthTokenInterface,
    EmailMagicLinkInterface,
    EmailOTPInterface,
    SmsOTPInterface,
    UserInterface,
    ValidationInterface,
)

from .config import Config

VERSION: str = "1.0.0"
CORBADO_HEADER_NAME = "X-Corbado-SDK"


class CorbadoSDK(BaseModel):
    """Entry point for the SDK"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    config: Config
    _api_client: Optional[ApiClient] = None

    _user_interface: Optional[UserInterface] = None
    _validation_interface: Optional[ValidationInterface] = None
    _sms_otp_interface: Optional[SmsOTPInterface] = None
    _email_otp_interface: Optional[EmailOTPInterface] = None
    _email_magic_link_interface: Optional[EmailMagicLinkInterface] = None
    _auth_token_interface: Optional[AuthTokenInterface] = None

    @property
    def api_client(self) -> ApiClient:
        """Get ApiClient

        Returns:
            ApiClient: ApiClient object.
        """
        if not self._api_client:
            self._api_client = ApiClient(configuration=self._create_generated_configuration())
            python_version: str = platform.python_version()

            data: dict[str, str] = {
                "name": "Python SDK",
                "sdkVersion": VERSION,
                "languageVersion": python_version,
            }
            self._api_client.set_default_header(header_name=CORBADO_HEADER_NAME, header_value=json.dumps(data))  # type: ignore
        return self._api_client

    # --------- Interfaces ---------------#
    @property
    def email_magic_link_interface(self) -> EmailMagicLinkInterface:
        """Get user EmailMagicLinkInterface

        Returns:
            EmailMagicLinkInterface: EmailMagicLinkInterface object.
        """
        if not self._email_magic_link_interface:
            self._email_magic_link_interface = EmailMagicLinkService(
                client=EmailMagicLinksApi(api_client=self.api_client)
            )
        return self._email_magic_link_interface

    @property
    def auth_token_interface(self) -> AuthTokenInterface:
        """Get user AuthTokenInterface

        Returns:
            AuthTokenInterface: AuthTokenInterface object.
        """
        if not self._auth_token_interface:
            self._auth_token_interface = AuthTokenService(client=AuthTokensApi(api_client=self.api_client))
        return self._auth_token_interface

    @property
    def user_interface(self) -> UserInterface:
        """Get user interface

        Returns:
            UserInterface: UserInterface object.
        """
        if not self._user_interface:
            self._user_interface = UserService(client=UserApi(api_client=self.api_client))

        return self._user_interface

    @property
    def email_otp_interface(self) -> EmailOTPInterface:
        """Get E-mail OTP interface

        Returns:
            EmailOTPInterface: EmailOTPInterface object.
        """
        if not self._email_otp_interface:
            self._email_otp_interface = EmailOTPService(client=EmailOTPApi(api_client=self.api_client))
        return self._email_otp_interface

    @property
    def sms_otp_interface(self) -> SmsOTPInterface:
        """Get SMS OTP interface

        Returns:
            SmsOTPInterface: SmsOTPInterface object.
        """
        if not self._sms_otp_interface:
            self._sms_otp_interface = SmsOTPService(client=SMSOTPApi(api_client=self.api_client))
        return self._sms_otp_interface

    @property
    def validation_interface(self) -> ValidationInterface:
        """Get validation interface

        Returns:
            ValidationInterface: ValidationInterface object.
        """
        if not self._validation_interface:
            self._validation_interface = ValidationService(client=ValidationApi(api_client=self.api_client))
        return self._validation_interface

    # ----------- Functions ----------#
    @validate_call
    def create_client_info(
        self,
        remote_address: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)],
        user_agent: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)],
    ) -> ClientInfo:
        """Creates client info

        Args:
            remote_address (Annotated[str, Field, optional): Defaults to 1, strict=True)] remote address.
            user_agent (Annotated[str, Field, optional): Defaults to 1)] user agent.

        Returns:
            ClientInfo: ClientInfo object.
        """

        client: ClientInfo = ClientInfo(remoteAddress=remote_address, userAgent=user_agent)
        return client

    def _create_generated_configuration(self) -> Configuration:
        """Creates configuration (generated class)

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
        """Generate basic auth header

        Args:
            username (str): ProjectId
            password (str): API Secret

        Returns:
            str: base64 encoded header value for basic authentication
        """
        credentials: str = f"{username}:{password}"
        encoded_credentials: str = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
