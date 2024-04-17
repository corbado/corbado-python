import json
import logging
import os
import unittest

from corbado_python_sdk import CorbadoSDK
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated.api.user_api import UserApi
from corbado_python_sdk.generated.api_client import ApiClient
from corbado_python_sdk.generated.configuration import Configuration
from corbado_python_sdk.generated.exceptions import BadRequestException
from corbado_python_sdk.generated.models.user_create_req import UserCreateReq
from corbado_python_sdk.generated.models.user_create_rsp import UserCreateRsp
from corbado_python_sdk.generated.models.user_list_rsp import UserListRsp
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()


class TestMisc(TestBase):

    def test_instantiate_sdk_expect_not_none(self) -> None:
        sdk: CorbadoSDK = self.sdk
        self.assertIsNotNone(obj=sdk)

    def test_list_users_expect_not_none(self) -> None:
        ret: UserListRsp = self.sdk.user_interface.list_users()
        self.assertIsNotNone(ret)

    def test_auth_method_manual_call(self) -> None:
        conf = Configuration(
            username=os.getenv(key=TestUtils.CORBADO_PROJECT_ID, default="missing CORBADO_PROJECT_ID"),
            password=os.getenv(key=TestUtils.CORBADO_API_SECRET, default="missing CORBADO_API_SECRET"),
            host=os.getenv(key=TestUtils.CORBADO_BACKEND_API, default="missing CORBADO_BACKEND_API"),
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


class UserCreateTest(TestBase):
    """
    Test cases for user creation.
    """

    def test_user_create_expect_validation_error(self):
        """
        Test case for user creation with validation error.
        """

        try:
            req: UserCreateReq = UserCreateReq(name="", email="")
            ret: UserCreateRsp = self.sdk.user_interface.create(request=req)
            logging.debug(f"Result: {ret}")
        except ServerException as e:
            self.assertIsNotNone(e)
            self.assertEqual(400, e.http_status_code)
            self.assertCountEqual(["name: cannot be blank"], e.get_validation_messages())

    def test_user_create_expect_success(self):
        """
        Test case for successful user creation.
        """

        req = UserCreateReq(name=TestUtils.create_random_test_name(), email=TestUtils.create_random_test_email())
        rsp: UserCreateRsp = self.sdk.user_interface.create(request=req)
        self.assertEqual(200, rsp.http_status_code)
