from typing import Annotated

from config import Config
from generated.configuration import Configuration
from generated.models.client_info import ClientInfo
from pydantic import BaseModel, Field, validate_call

VERSION: str = "3.0.1"


class CorbadoSDK(BaseModel):
    config: Config

    @validate_call
    def create_client_info(
        self,
        remote_address: Annotated[str, Field(min_length=1, strict=True)],
        user_agent: Annotated[str, Field(min_length=1)],
    ) -> ClientInfo:

        # Assert::stringNotEmpty($remoteAddress);
        client: ClientInfo = ClientInfo(
            remoteAddress=remote_address, userAgent=user_agent
        )
        return client

    def create_generated_configuration(self) -> Configuration:
        _config: Configuration = Configuration(
            host=config.backend_api,
            username=config.project_id,
            password=config.project_id,
            access_token=None,
        )
        return _config


config = Config(project_id="pro-2", api_secret="corbado1_12345")
sdk = CorbadoSDK(config=config)
ret: ClientInfo = sdk.create_client_info(remote_address="1234", user_agent=" ")
print(ret)
