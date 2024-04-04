import json
import platform
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, validate_call
from typing_extensions import Annotated

from corbado_python_sdk.generated.api.user_api import UserApi
from corbado_python_sdk.generated.api_client import ApiClient
from corbado_python_sdk.generated.configuration import Configuration
from corbado_python_sdk.generated.models.client_info import ClientInfo
from corbado_python_sdk.services.user_interface import UserInterface
from corbado_python_sdk.services.user_service import UserService

from .config import Config

VERSION: str = "1.0.0"
CORBADO_HEADER_NAME = "X-Corbado-SDK"


class CorbadoSDK(BaseModel):
    """Entry point for the SDK"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    config: Config
    _user_interface: Optional[UserInterface] = None
    _api_client: Optional[ApiClient] = None

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

    # Interfaces
    @property
    def user_interface(self) -> UserInterface:
        """Get user interface

        Returns:
            UserInterface: UserInterface object.
        """
        if not self._user_interface:
            self._user_interface = UserService(client=UserApi(api_client=self.api_client))
        return self._user_interface

    # Functions
    @validate_call
    def create_client_info(
        self,
        remote_address: Annotated[str, Field(min_length=1, strict=True)],
        user_agent: Annotated[str, Field(min_length=1)],
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
        )


# Services
