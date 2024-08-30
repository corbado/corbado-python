import os
import random
import string

from typing_extensions import LiteralString

from corbado_python_sdk import CorbadoSDK, UserStatus
from corbado_python_sdk.config import Config
from corbado_python_sdk.entities import UserEntity
from corbado_python_sdk.generated import UserCreateReq


class TestUtils:
    """Utility class for test."""

    CORBADO_API_SECRET: str = "CORBADO_API_SECRET"
    CORBADO_PROJECT_ID: str = "CORBADO_PROJECT_ID"
    CORBADO_BACKEND_API: str = "CORBADO_BACKEND_API"

    @classmethod
    def instantiate_sdk(cls) -> CorbadoSDK:
        """Instantiate SDK with parameters from environment variables."""
        config: Config = Config(
            api_secret=os.getenv(key=TestUtils.CORBADO_API_SECRET, default="missing CORBADO_API_SECRET"),
            project_id=os.getenv(key=TestUtils.CORBADO_PROJECT_ID, default="missing CORBADO_PROJECT_ID"),
            backend_api=os.getenv(key=TestUtils.CORBADO_BACKEND_API, default="https://backendapi.cloud.corbado.io/v2"),
        )
        return CorbadoSDK(config=config)

    @classmethod
    def generate_string(cls, length: int, characters: str) -> str:
        """Generate a random string of specified length using the provided characters."""
        return "".join(random.choice(characters) for _ in range(length))

    @classmethod
    def create_random_test_name(cls) -> str:
        """Generate a random test name."""
        characters: LiteralString = string.ascii_letters + string.digits
        return TestUtils.generate_string(10, characters)

    @classmethod
    def create_random_test_email(cls) -> str:
        """Generate a random test email."""
        characters: LiteralString = string.ascii_letters + string.digits
        random_string = TestUtils.generate_string(10, characters)
        return f"integration-test+{random_string}@corbado.com"

    @classmethod
    def create_random_test_phone_number(cls) -> str:
        """Generate a random test phone number."""
        return "+491509" + TestUtils.generate_string(7, string.digits)

    @classmethod
    def create_user(cls) -> UserEntity:
        """Create a user and return the user ID."""
        req = UserCreateReq(fullName=TestUtils.create_random_test_name(), status=UserStatus.ACTIVE)
        rsp: UserEntity = TestUtils.instantiate_sdk().users.create_from_request(request=req)
        return rsp
