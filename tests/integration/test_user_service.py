import unittest

from corbado_python_sdk import CorbadoSDK, UserEntity, UserStatus
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.services.implementation import UserService
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: UserService = cls.sdk.users


class TestMisc(TestBase):

    def test_instantiate_sdk_expect_not_none(self) -> None:
        sdk: CorbadoSDK = self.sdk
        self.assertIsNotNone(obj=sdk)


class UserCreateTest(TestBase):
    """Test cases for user creation."""

    def test_user_create_expect_success(self) -> None:
        """Test case for successful user creation."""
        test_status = UserStatus.ACTIVE
        test_name: str = TestUtils.create_random_test_name()
        rsp: UserEntity = self.fixture.create(status=test_status, full_name=test_name)

        self.assertEqual(first=test_status, second=rsp.status)
        self.assertEqual(first=test_name, second=rsp.full_name)


class TestUserDelete(TestBase):
    """Tests for the user deletion functionality."""

    def test_user_delete_expect_not_found(self) -> None:
        """Test for deleting a user that does not exist."""
        with self.assertRaises(expected_exception=ServerException) as context:
            self.fixture.delete(user_id="usr-123456789")

        e: ServerException = context.exception
        self.assertIsNotNone(e)
        self.assertEqual(400, e.http_status_code)
        self.assertListEqual(["userID: does not exist"], e.validation_messages)

    def test_user_delete_expect_success(self) -> None:
        """Test for successfully deleting a user."""
        user: UserEntity = TestUtils.create_user()

        self.fixture.delete(user_id=user.user_id)


class TestUserGet(TestBase):
    """Tests for the user retrieval functionality."""

    def test_user_get_expect_not_found(self) -> None:
        """Test for retrieving a user that does not exist."""
        with self.assertRaises(expected_exception=ServerException) as context:
            self.fixture.get(user_id="usr-123456789")

        e: ServerException = context.exception
        self.assertIsNotNone(e)
        self.assertEqual(400, e.http_status_code)

    def test_user_get_expect_success(self) -> None:
        """Test for successfully retrieving a user."""
        user: UserEntity = TestUtils.create_user()

        rsp: UserEntity = self.fixture.get(user_id=user.user_id)
        self.assertEqual(first=user, second=rsp)
