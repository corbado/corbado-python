import os

from corbado_python_sdk.config import Config
from corbado_python_sdk.corbado_sdk import CorbadoSDK


class TestUtils:
    CORBADO_API_SECRET: str = "CORBADO_API_SECRET"
    CORBADO_PROJECT_ID: str = "CORBADO_PROJECT_ID"

    @classmethod
    def instantiate_sdk(cls) -> CorbadoSDK:
        config: Config = Config(
            api_secret=os.getenv(key=TestUtils.CORBADO_API_SECRET, default="missing CORBADO_API_SECRET"),
            project_id=os.getenv(key=TestUtils.CORBADO_PROJECT_ID, default="missing CORBADO_PROJECT_ID"),
        )
        return CorbadoSDK(config=config)
