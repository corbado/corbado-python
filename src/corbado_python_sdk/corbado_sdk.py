from typing import Annotated

from config import Config
from generated.configuration import Configuration
from generated.models.client_info import ClientInfo
from pydantic import BaseModel, Field, validate_call

VERSION: str = "3.0.1"


class CorbadoSDK(BaseModel):
    """Entry point for the SDK"""

    config: Config

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

    def create_generated_configuration(self) -> Configuration:
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
