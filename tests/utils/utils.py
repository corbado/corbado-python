import os
import random
import string

from typing_extensions import LiteralString

from corbado_python_sdk import CorbadoSDK
from corbado_python_sdk.config import Config
from corbado_python_sdk.generated import UserCreateReq
from corbado_python_sdk.generated.models.user_create_rsp import UserCreateRsp


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
    def create_user(cls) -> str:
        """Create a user and return the user ID."""
        req = UserCreateReq(name=TestUtils.create_random_test_name(), email=TestUtils.create_random_test_email())
        rsp: UserCreateRsp = TestUtils.instantiate_sdk().user_interface.create(request=req)
        return rsp.data.user_id
