import json
import os
import unittest

from corbado_python_sdk.corbado_sdk import CorbadoSDK
from corbado_python_sdk.generated.api.user_api import UserApi
from corbado_python_sdk.generated.api_client import ApiClient
from corbado_python_sdk.generated.configuration import Configuration
from corbado_python_sdk.generated.exceptions import BadRequestException
from corbado_python_sdk.generated.models.user_create_req import UserCreateReq
from corbado_python_sdk.generated.models.user_create_rsp import UserCreateRsp
from corbado_python_sdk.generated.models.user_list_rsp import UserListRsp
from tests.utils import TestUtils


class TestAuthMethod(unittest.TestCase):
    print("First Test")
    assert 2 * 2 == 4

    def test_instantiate_sdk(self) -> None:
        sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        self.assertIsNotNone(obj=sdk)

    def test_list_users(self) -> None:
        ret: UserListRsp = TestUtils.instantiate_sdk().user_interface.list_users()
        self.assertIsNotNone(ret)

    def test_auth_method_manual_call(self):
        conf = Configuration(
            username=os.getenv(key=TestUtils.CORBADO_PROJECT_ID, default="missing CORBADO_PROJECT_ID"),
            password=os.getenv(key=TestUtils.CORBADO_API_SECRET, default="missing CORBADO_API_SECRET"),
        )
        client = ApiClient(
            configuration=conf,
        )
        user_api = UserApi(api_client=client)
        ret: UserListRsp = user_api.user_list()
        print("Getting Users")
        for user in ret.data.users:
            print(f"Name: {user.full_name}, Email: {user.emails[0].email}, Creation Date: {user.created}")

        create_request = UserCreateReq(
            name="FullNameCreate",
            fullName="CreateRequestTestName",
            email="test3@python.com",
        )
        print("Creating existing client")
        try:
            create_response: UserCreateRsp = user_api.user_create(user_create_req=create_request)
            print(f"Create response: {create_response}")
        except BadRequestException as e:
            print("Exception type:", type(e))
            data = json.loads(e.body)
            print(data)
