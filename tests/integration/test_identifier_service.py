import unittest
from typing import List

from pytest import fixture

from corbado_python_sdk import (
    CorbadoSDK,
    Identifier,
    IdentifierCreateReq,
    IdentifierStatus,
    IdentifierType,
    UserEntity,
    UserStatus,
)
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.services.implementation import IdentifierService
from corbado_python_sdk.services.interface import IdentifierInterface
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    TEST_USER_ID: str
    TEST_USER_EMAIL: str
    TEST_USER_PHONE: str
    TEST_USER_EMAIL_IDENTIFIER: Identifier

    @classmethod
    def setUpClass(cls):
        """Set up test class with necessary data."""
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: IdentifierInterface = cls.sdk.identifiers
        print(cls.fixture)

        cls.TEST_USER_ID = TestUtils.create_user().user_id
        cls.TEST_USER_EMAIL = TestUtils.create_random_test_email()
        cls.TEST_USER_PHONE = TestUtils.create_random_test_phone_number()

        cls.TEST_USER_EMAIL_IDENTIFIER = cls.fixture.create(
            user_id=cls.TEST_USER_ID,
            identifier_type=IdentifierType.EMAIL,
            identifier_value=cls.TEST_USER_EMAIL,
            status=IdentifierStatus.PRIMARY,
        )

        cls.fixture.create(
            user_id=cls.TEST_USER_ID,
            identifier_type=IdentifierType.PHONE,
            identifier_value=cls.TEST_USER_PHONE,
            status=IdentifierStatus.PRIMARY,
        )


class TestIdentifierService(TestBase):
    """Test cases for IdentifierService."""

    def assert_validation_error_equals(self, exc: ServerException, field: str, message: str):
        """Helper to assert validation errors."""
        assert len(exc.validation_messages) == 1
        assert exc.validation_messages[0] == field
        assert exc.validation_messages[0] == message

    def test_check_existing_email_is_present_expect_success(self):
        """Test getting email and non-matching phone identifiers."""
        ret = self.fixture.list_by_value_and_type(value=self.TEST_USER_EMAIL, identifier_type=IdentifierType.EMAIL)
        assert len(ret.identifiers) != 0

        ret = self.fixture.list_by_value_and_type(value=self.TEST_USER_EMAIL, identifier_type=IdentifierType.PHONE)
        assert not self.fixture.exists_by_value_and_type(value=self.TEST_USER_EMAIL, identifier_type=IdentifierType.PHONE)
        assert len(ret.identifiers) == 0

    def test_create_empty_identifier_expect_exception(self):
        """Test creating an empty identifier and expecting an exception."""
        user_id = TestUtils.create_user().user_id
        email = ""
        with pytest.raises(ServerException) as excinfo:
            self.fixture.create(
                user_id=user_id, identifier_type=IdentifierType.EMAIL, identifier_value=email, status=IdentifierStatus.PRIMARY
            )
        self.assert_validation_error_equals(excinfo.value, "identifierValue", TestUtils.CANNOT_BE_BLANK_MESSAGE)

    def test_create_identifier_expect_success(self):
        """Test creating an identifier successfully."""
        user_id = TestUtils.create_user().user_id
        email: str = TestUtils.create_random_test_email()
        rsp: Identifier = self.fixture.create(
            user_id=user_id, identifier_type=IdentifierType.EMAIL, identifier_value=email, status=IdentifierStatus.PRIMARY
        )
        assert rsp.user_id == user_id
        assert rsp.value == email
        assert rsp.type == IdentifierType.EMAIL

    def test_get_identifiers_for_user_id_expect_list_of_identifiers(self):
        """Test case for searching identifiers by user ID."""
        ret = self.fixture.list_all_by_user_id_with_paging(user_id=self.TEST_USER_ID, page=None, page_size=None)
        assert any(x.identifier_id == self.TEST_USER_EMAIL_IDENTIFIER.identifier_id for x in ret.identifiers)
        assert len(ret.identifiers) == 2

    def test_list_identifiers_all_expect_success(self):
        """Test listing all identifiers with success."""
        ret = self.fixture.list(sort=None, filter=None, page=None, page_size=100)
        assert ret is not None

    def test_update_identifier_expect_success(self):
        """Test updating an identifier's status."""
        self.fixture.update_status(
            user_id=self.TEST_USER_EMAIL_IDENTIFIER.user_id,
            identifier_id=self.TEST_USER_EMAIL_IDENTIFIER.identifier_id,
            status=IdentifierStatus.PENDING,
        )
        ret = self.fixture.list_by_value_and_type(
            value=self.TEST_USER_EMAIL_IDENTIFIER.value, identifier_type=self.TEST_USER_EMAIL_IDENTIFIER.type
        )
        assert ret.identifiers[0].status == IdentifierStatus.PENDING

        self.fixture.update_status(
            user_id=self.TEST_USER_EMAIL_IDENTIFIER.user_id,
            identifier_id=self.TEST_USER_EMAIL_IDENTIFIER.identifier_id,
            status=IdentifierStatus.PRIMARY,
        )
        ret = self.fixture.list_by_value_and_type(
            value=self.TEST_USER_EMAIL_IDENTIFIER.value, identifier_type=self.TEST_USER_EMAIL_IDENTIFIER.type
        )
        assert ret.identifiers[0].status == IdentifierStatus.PRIMARY

    def test_list_all_emails_by_user_id_expect_success(self):
        """Test listing all emails by user ID with success."""
        test_size = 21
        for _ in range(test_size):
            self.fixture.create(
                user_id=self.TEST_USER_ID,
                identifier_type=IdentifierType.EMAIL,
                identifier_value=TestUtils.create_random_test_email(),
                status=IdentifierStatus.VERIFIED,
            )

        ret: List[Identifier] = self.fixture.list_all_emails_by_user_id(user_id=self.TEST_USER_ID)
        assert len(ret) == test_size + 1
