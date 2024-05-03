import unittest

from pydantic import ValidationError

from corbado_python_sdk import CorbadoSDK
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated.models import EmailCodeSendReq, EmailCodeValidateReq
from corbado_python_sdk.generated.models.email_code_send_rsp import EmailCodeSendRsp
from corbado_python_sdk.services.interface import EmailOTPInterface
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: EmailOTPInterface = cls.sdk.email_otp_interface


class EmailOTPSendTest(TestBase):
    """Test cases for sending email OTP."""

    def test_email_otp_send_blank_email_expect_validation_error(self):
        """Test case to validate the email OTP sending with invalid input."""
        req = EmailCodeSendReq(email=" ", create=True)

        with self.assertRaises(ServerException) as context:
            self.fixture.send(req)

        self.assertIsNotNone(context.exception)
        self.assertCountEqual(["email: cannot be blank"], context.exception.get_validation_messages())

    def test_email_otp_send_success(self):
        """Test case to validate the successful sending of email OTP."""
        req = EmailCodeSendReq(email=TestUtils.create_random_test_email(), create=True)

        rsp: EmailCodeSendRsp = self.fixture.send(req)
        self.assertEqual(200, rsp.http_status_code)


class TestEmailOTPValidate(TestBase):
    def test_email_otp_validate_expect_validation_error_string_too_short(self):
        with self.assertRaises(expected_exception=ValidationError) as cm:
            req = EmailCodeValidateReq(code="")
            self.fixture.validate_email("   ", req)
        self.assertTrue(any(error.get("type") == "string_too_short" for error in cm.exception.errors()))

    def test_email_otp_validate_expect_validation_error_empty_code(self):
        with self.assertRaises(expected_exception=ServerException) as cm:
            req = EmailCodeValidateReq(code="")
            self.fixture.validate_email("emc-123456789", req)
        self.assertEqual(cm.exception.get_validation_messages(), ["code: cannot be blank"])

    def test_email_otp_validate_expect_validation_error_invalid_code(self):
        with self.assertRaises(expected_exception=ServerException) as cm:
            req = EmailCodeValidateReq(code="1")
            self.fixture.validate_email("emc-123456789", req)
        self.assertEqual(cm.exception.get_validation_messages(), ["code: the length must be exactly 6"])

    def test_email_otp_validate_expect_validation_error_invalid_id(self):
        with self.assertRaises(ServerException) as cm:
            req = EmailCodeValidateReq(code="123456")
            self.fixture.validate_email("emc-123456789", req)
        self.assertEqual(cm.exception.http_status_code, 404)

    def test_email_otp_expect_validate_success(self):
        req = EmailCodeSendReq(email=TestUtils.create_random_test_email(), create=True)
        rsp = self.fixture.send(req)
        self.assertEqual(rsp.http_status_code, 200)

        req = EmailCodeValidateReq(code="150919")
        self.fixture.validate_email(rsp.data.email_code_id, req)
