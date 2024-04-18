import unittest

from corbado_python_sdk import CorbadoSDK
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated.models import (
    UserCreateReq,
    UserCreateRsp,
    UserDeleteReq,
    UserListRsp,
)
from corbado_python_sdk.generated.models.generic_rsp import GenericRsp
from corbado_python_sdk.generated.models.user_get_rsp import UserGetRsp
from corbado_python_sdk.services.interface.user_interface import UserInterface
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: UserInterface = cls.sdk.user_interface


class TestMisc(TestBase):

    def test_instantiate_sdk_expect_not_none(self) -> None:
        sdk: CorbadoSDK = self.sdk
        self.assertIsNotNone(obj=sdk)

    def test_list_users_expect_not_none(self) -> None:
        ret: UserListRsp = self.fixture.list_users()
        self.assertIsNotNone(ret)


class UserCreateTest(TestBase):
    """
    Test cases for user creation.
    """

    def test_user_create_blank_name_expect_validation_error(self):
        """
        Test case for user creation with validation error.
        """

        with self.assertRaises(ServerException) as context:
            req: UserCreateReq = UserCreateReq(name="", email="")
            self.fixture.create(request=req)

        e: ServerException = context.exception
        self.assertIsNotNone(e)
        self.assertEqual(400, e.http_status_code)
        self.assertCountEqual(["name: cannot be blank"], e.get_validation_messages())

    def test_user_create_expect_success(self):
        """
        Test case for successful user creation.
        """

        req = UserCreateReq(name=TestUtils.create_random_test_name(), email=TestUtils.create_random_test_email())
        rsp: UserCreateRsp = self.fixture.create(request=req)
        self.assertEqual(200, rsp.http_status_code)


class TestUserDelete(TestBase):
    """
    Tests for the user deletion functionality.
    """

    def test_user_delete_expect_not_found(self) -> None:
        """
        Test for deleting a user that does not exist.
        """
        with self.assertRaises(ServerException) as context:
            self.fixture.delete(user_id="usr-123456789", request=UserDeleteReq())

        e: ServerException = context.exception
        self.assertIsNotNone(e)
        self.assertEqual(400, e.http_status_code)
        self.assertListEqual(["userID: does not exist"], e.get_validation_messages())

    def test_user_delete_expect_success(self) -> None:
        """
        Test for successfully deleting a user.

        """
        user_id: str = TestUtils.create_user()

        rsp: GenericRsp = self.fixture.delete(user_id, UserDeleteReq())
        self.assertEqual(200, rsp.http_status_code)


class TestUserGet(TestBase):
    """
    Tests for the user retrieval functionality.
    """

    def test_user_get_expect_not_found(self) -> None:
        """
        Test for retrieving a user that does not exist.
        """
        with self.assertRaises(ServerException) as context:
            self.fixture.get(user_id="usr-123456789")

        e: ServerException = context.exception
        self.assertIsNotNone(e)
        self.assertEqual(404, e.http_status_code)

    def test_user_get_expect_success(self) -> None:
        """
        Test for successfully retrieving a user.

        """
        user_id: str = TestUtils.create_user()

        rsp: UserGetRsp = self.fixture.get(user_id=user_id)
        self.assertEqual(200, rsp.http_status_code)


class TestUserList(TestBase):
    """
    Tests for the user listing functionality.
    """

    def test_user_list_invalid_sort_expect_validation_error(self) -> None:
        """
        Test for listing users with validation error.
        """
        with self.assertRaises(ServerException) as context:
            self.fixture.list_users(remote_addr="", user_agent="", sort="foo:bar")

        e: ServerException = context.exception
        self.assertIsNotNone(e)
        self.assertEqual(422, e.http_status_code)
        self.assertListEqual(["sort: Invalid order direction 'bar'"], e.get_validation_messages())

    def test_user_list_success(self) -> None:
        """
        Test for successfully listing users.

        """
        user_id: str = TestUtils.create_user()
        rsp: UserListRsp = self.fixture.list_users(remote_addr="", user_agent="", sort="created:desc")

        found: bool = False
        for user in rsp.data.users:
            if user.id == user_id:
                found = True
                break

        self.assertTrue(found)
