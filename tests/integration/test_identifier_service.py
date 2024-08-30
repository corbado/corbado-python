import logging
import unittest

from typing_extensions import List

from corbado_python_sdk import CorbadoSDK, Identifier, IdentifierStatus, IdentifierType
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated.models.identifier_list import IdentifierList
from corbado_python_sdk.services.implementation.identifier_service import (
    IdentifierService,
)
from tests.utils import TestUtils

CANNOT_BE_BLANK = "cannot be blank"
logging.basicConfig(level=logging.DEBUG)
urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.DEBUG)


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test class with necessary data."""
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: IdentifierService = cls.sdk.identifiers

        cls.TEST_USER_ID = TestUtils.create_user().user_id
        cls.TEST_USER_EMAIL: str = TestUtils.create_random_test_email()
        cls.TEST_USER_PHONE: str = TestUtils.create_random_test_phone_number()

        cls.TEST_USER_EMAIL_IDENTIFIER: Identifier = cls.fixture.create(
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

    def test_check_existing_email_is_present_expect_success(self):
        """Test getting email and non-matching phone identifiers."""
        ret: IdentifierList = self.fixture.list_identifiers(
            identifier_type=IdentifierType.EMAIL, identifier_value=self.TEST_USER_EMAIL
        )
        self.assertEqual(first=1, second=ret.paging.total_items)  # assert only one TEST_USER_EMAIL exists in list

        self.assertFalse(
            self.fixture.exists_by_value_and_type(
                value=self.TEST_USER_EMAIL,
                identifier_type=IdentifierType.PHONE,  # assert Identifier Type works correctly
            )
        )
        self.assertTrue(
            expr=self.fixture.exists_by_value_and_type(
                value=self.TEST_USER_EMAIL, identifier_type=IdentifierType.EMAIL
            )  # assert Identifier Type works correctly
        )

    def test_create_empty_identifier_expect_exception(self):
        """Test creating an empty identifier and expecting an exception."""
        user_id = TestUtils.create_user().user_id
        email = ""

        with self.assertRaises(expected_exception=ServerException) as context:
            self.fixture.create(
                user_id=user_id,
                identifier_type=IdentifierType.EMAIL,
                identifier_value=email,
                status=IdentifierStatus.PRIMARY,
            )
        e: ServerException = context.exception
        self.assertIsNotNone(e)
        self.assertEqual(e.validation_messages[0], second="identifierValue: cannot be blank")

    def test_create_identifier_expect_success(self):
        """Test creating an identifier successfully."""
        user_id = TestUtils.create_user().user_id
        email: str = TestUtils.create_random_test_email()
        rsp: Identifier = self.fixture.create(
            user_id=user_id,
            identifier_type=IdentifierType.EMAIL,
            identifier_value=email,
            status=IdentifierStatus.PRIMARY,
        )
        self.assertEqual(user_id, rsp.user_id)
        self.assertEqual(email, rsp.value)
        self.assertEqual(IdentifierType.EMAIL, rsp.type)

    def test_get_identifiers_for_user_id_expect_list_of_identifiers(self):
        """Test case for searching identifiers by user ID."""
        ret: IdentifierList = self.fixture.list_identifiers(user_id=self.TEST_USER_ID)
        any(x.identifier_id == self.TEST_USER_EMAIL_IDENTIFIER.identifier_id for x in ret.identifiers)
        self.assertEqual(2, len(ret.identifiers))

    def test_list_identifiers_all_expect_success(self):
        """Test listing all identifiers with success."""
        ret: IdentifierList = self.fixture.list_identifiers(sort=None, page_size=100)
        self.assertIsNotNone(ret)

    def test_update_identifier_expect_success(self):
        """Test updating an identifier's status."""
        self.fixture.update_status(
            user_id=self.TEST_USER_EMAIL_IDENTIFIER.user_id,
            identifier_id=self.TEST_USER_EMAIL_IDENTIFIER.identifier_id,
            status=IdentifierStatus.PENDING,
        )
        ret: IdentifierList = self.fixture.list_identifiers(
            identifier_value=self.TEST_USER_EMAIL_IDENTIFIER.value, identifier_type=self.TEST_USER_EMAIL_IDENTIFIER.type
        )
        assert ret.identifiers[0].status == IdentifierStatus.PENDING

        self.fixture.update_status(
            user_id=self.TEST_USER_EMAIL_IDENTIFIER.user_id,
            identifier_id=self.TEST_USER_EMAIL_IDENTIFIER.identifier_id,
            status=IdentifierStatus.PRIMARY,
        )
        ret = self.fixture.list_identifiers(
            identifier_value=self.TEST_USER_EMAIL_IDENTIFIER.value, identifier_type=self.TEST_USER_EMAIL_IDENTIFIER.type
        )
        self.assertEqual(IdentifierStatus.PRIMARY, ret.identifiers[0].status)

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
        self.assertEqual(first=test_size + 1, second=len(ret))

    def test_delete_expect_success(self):
        identifier_created: Identifier = self.fixture.create(
            user_id=self.TEST_USER_ID,
            identifier_type=IdentifierType.EMAIL,
            identifier_value=TestUtils.create_random_test_email(),
            status=IdentifierStatus.VERIFIED,
        )
        self.fixture.delete(identifier_id=identifier_created.identifier_id, user_id=identifier_created.user_id)
