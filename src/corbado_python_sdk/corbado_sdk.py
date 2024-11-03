import base64
import json
import platform
from importlib.metadata import version

from pydantic import BaseModel, ConfigDict
from typing_extensions import Dict, Optional

from corbado_python_sdk import Config
from corbado_python_sdk.generated.api import IdentifiersApi, UsersApi
from corbado_python_sdk.generated.api_client import ApiClient
from corbado_python_sdk.generated.configuration import Configuration
from corbado_python_sdk.services.implementation import (
    IdentifierService,
    SessionService,
    UserService,
)

CORBADO_HEADER_NAME = "X-Corbado-SDK"


class CorbadoSDK(BaseModel):
    """
    Entry point for the Corbado SDK.

    This class provides various interfaces to interact with the Corbado API,
    including user management, session handling, validation, and OTP services.

    Attributes:
        config (Config): The configuration object for the SDK.
        api_client (ApiClient): The API client used to make requests to the backend API.
        sessions (SessionService): The session service service.
        users (UserService): The user service.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    config: Config
    _api_client: Optional[ApiClient] = None
    _sessions: Optional[SessionService] = None
    _users: Optional[UserService] = None
    _identifiers: Optional[IdentifierService] = None

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
                "sdkVersion": version(distribution_name="passkeys"),
                "languageVersion": python_version,
            }
            self._api_client.set_default_header(header_name=CORBADO_HEADER_NAME, header_value=json.dumps(data))  # type: ignore
        return self._api_client

    # --------- Services ---------------#
    @property
    def sessions(self) -> SessionService:
        """Get user SessionService.

        Returns:
            SessionService: SessionService object.
        """
        if not self._sessions:
            self._sessions = SessionService(
                issuer=self.config.issuer,
                jwks_uri=self.config.frontend_api + "/.well-known/jwks",
                project_id=self.config.project_id,
            )

        return self._sessions

    @property
    def users(self) -> UserService:
        """Get user service.

        Returns:
            UserService: UserService object.
        """
        if not self._users:
            client = UsersApi(api_client=self.api_client)
            self._users = UserService(client=client)

        return self._users

    @property
    def identifiers(self) -> IdentifierService:
        """Get identifier service.

        Returns:
            IdentifierService: IdentifierService object.
        """
        if not self._identifiers:
            client = IdentifiersApi(api_client=self.api_client)
            self._identifiers = IdentifierService(client=client)

        return self._identifiers

    # ----------- Functions ----------#

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
