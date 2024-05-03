import unittest

from corbado_python_sdk import CorbadoSDK
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated.models import ValidateEmailReq, ValidatePhoneNumberReq
from corbado_python_sdk.generated.models.validate_email_rsp import ValidateEmailRsp
from corbado_python_sdk.generated.models.validate_phone_number_rsp import (
    ValidatePhoneNumberRsp,
)
from corbado_python_sdk.services.interface.validation_interface import (
    ValidationInterface,
)
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: ValidationInterface = cls.sdk.validation_interface


class ValidateEmailTest(TestBase):
    """Test cases for email validation."""

    def test_validate_blank_email_validation_error(self) -> None:
        """Test for email validation error."""
        with self.assertRaises(ServerException) as context:
            req = ValidateEmailReq(email="")
            self.fixture.validate_email(req)

        e: ServerException = context.exception
        self.assertIsNotNone(e)
        self.assertEqual(400, e.http_status_code)
        self.assertListEqual(["email: cannot be blank"], e.get_validation_messages())

    def test_validate_email_success(self) -> None:
        """Test for successful email validation."""
        req = ValidateEmailReq(email="info@corbado.com")

        rsp: ValidateEmailRsp = self.fixture.validate_email(req)
        self.assertTrue(rsp.data.is_valid)


class ValidatePhoneNumberTest(TestBase):
    """Test case for validating phone numbers."""

    def test_validate_phone_number_validation_error(self):
        """Test case for validating phone number with empty input."""
        with self.assertRaises(expected_exception=ServerException) as context:
            req = ValidatePhoneNumberReq(phoneNumber="")
            self.fixture.validate_phone_number(req)

        exception = context.exception
        self.assertIsNotNone(exception)
        self.assertEqual(400, exception.http_status_code)
        self.assertCountEqual(["phoneNumber: cannot be blank"], exception.get_validation_messages())

    def test_validate_phone_number_success(self):
        req = ValidatePhoneNumberReq(phoneNumber="+49 151 12345678")
        rsp: ValidatePhoneNumberRsp = self.fixture.validate_phone_number(req)
        self.assertTrue(rsp.data.is_valid)
