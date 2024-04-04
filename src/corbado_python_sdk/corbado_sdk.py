from pydantic import BaseModel, Field, validate_call
from typing_extensions import Annotated

from corbado_python_sdk.generated.configuration import Configuration
from corbado_python_sdk.generated.models.client_info import ClientInfo
from corbado_python_sdk.services.user_service import UserInterface

from .config import Config

VERSION: str = "3.0.1"


class CorbadoSDK(BaseModel):
    """Entry point for the SDK"""

    user_interface: UserInterface
    config: Config

    def __init__(self, config: Config) -> None:
        # client =
        self._config: Config = config

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
            ClientInfo: client info
        """

        client: ClientInfo = ClientInfo(remoteAddress=remote_address, userAgent=user_agent)
        return client

    def _create_generated_configuration(self) -> Configuration:
        """Creates configuration (generated class)

        Returns:
            Configuration: configuration
        """
        return Configuration(
            host=self.config.backend_api,
            username=self.config.project_id,
            password=self.config.project_id,
            access_token=None,
        )


# Services
