import os

from corbado_python_sdk.config import Config
from corbado_python_sdk.corbado_sdk import CorbadoSDK


class TestUtils:
    CORBADO_API_SECRET: str = "CORBADO_API_SECRET"
    CORBADO_PROJECT_ID: str = "CORBADO_PROJECT_ID"
    CORBADO_BACKEND_API: str = "CORBADO_BACKEND_API"

    @classmethod
    def instantiate_sdk(cls) -> CorbadoSDK:
        config: Config = Config(
            api_secret=os.getenv(key=TestUtils.CORBADO_API_SECRET, default="missing CORBADO_API_SECRET"),
            project_id=os.getenv(key=TestUtils.CORBADO_PROJECT_ID, default="missing CORBADO_PROJECT_ID"),
            backend_api=os.getenv(key=TestUtils.CORBADO_BACKEND_API, default="missing CORBADO_BACKEND_API"),
        )
        return CorbadoSDK(config=config)
