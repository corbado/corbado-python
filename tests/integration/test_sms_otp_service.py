import unittest

from corbado_python_sdk import CorbadoSDK
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated.models import (
    SmsCodeSendReq,
    SmsCodeSendRsp,
    SmsCodeValidateReq,
)
from corbado_python_sdk.services.interface import SmsOTPInterface
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: SmsOTPInterface = cls.sdk.sms_otps


class SmsOTPSendTest(TestBase):
    """Test cases for sending SMS OTP codes."""

    def test_sms_otp_send_expect_validation_error(self):
        """Test case for sending SMS OTP code with validation error."""
        try:
            req = SmsCodeSendReq(phoneNumber="", create=True)
            self.fixture.send(req)
            self.fail(msg="Expected an exception")
        except ServerException as e:
            self.assertIsNotNone(e)
            self.assertCountEqual(["phoneNumber: cannot be blank"], e.validation_messages)

    def test_sms_otp_send_success(self):
        """Test case for successful sending of SMS OTP code."""
        req = SmsCodeSendReq(phoneNumber=TestUtils.create_random_test_phone_number(), create=True)
        rsp: SmsCodeSendRsp = self.fixture.send(req)
        self.assertEqual(200, rsp.http_status_code)


class SmsOTPValidateTest(TestBase):
    """Test cases for validating SMS OTP codes."""

    def test_sms_otp_validate_blank_expect_error_empty_code(self):
        """Test case for validating SMS OTP code with empty code."""
        req = SmsCodeValidateReq(smsCode="")

        with self.assertRaises(ServerException) as context:
            self.fixture.validate_sms("sms-123456789", req)

        self.assertIsNotNone(context.exception)
        self.assertCountEqual(["smsCode: cannot be blank"], context.exception.validation_messages)

    def test_sms_otp_validate_invalid_length_expect_error_invalid_code(self):
        """Test case for validating SMS OTP code with invalid code."""
        req = SmsCodeValidateReq(smsCode="1")

        with self.assertRaises(ServerException) as context:
            self.fixture.validate_sms("sms-123456789", req)

        self.assertIsNotNone(context.exception)
        self.assertCountEqual(["smsCode: the length must be exactly 6"], context.exception.validation_messages)

    def test_sms_otp_validate_invalid_id_expect_error_invalid_id(self):
        """Test case for validating SMS OTP code with invalid ID."""
        req = SmsCodeValidateReq(smsCode="123456")

        with self.assertRaises(ServerException) as context:
            self.fixture.validate_sms("sms-123456789", req)

        self.assertIsNotNone(context.exception)
        self.assertEqual(404, context.exception.http_status_code)

    def test_sms_otp_validate_expect_success(self):
        """Test case for successful validation of SMS OTP code."""
        req = SmsCodeSendReq(phoneNumber=TestUtils().create_random_test_phone_number(), create=True)
        rsp: SmsCodeSendRsp = self.fixture.send(req)
        self.assertEqual(200, rsp.http_status_code)

        req = SmsCodeValidateReq(smsCode="150919")
        self.fixture.validate_sms(rsp.data.sms_code_id, req)
