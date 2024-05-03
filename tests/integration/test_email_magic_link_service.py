import unittest

from corbado_python_sdk import CorbadoSDK
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated.models import EmailLinkSendReq, EmailLinksValidateReq
from corbado_python_sdk.generated.models.email_link_send_rsp import EmailLinkSendRsp
from corbado_python_sdk.services.interface import EmailMagicLinkInterface
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: EmailMagicLinkInterface = cls.sdk.email_magic_link_interface


class EmailMagicLinkSendTest(TestBase):
    """Test case for sending email magic links."""

    def test_email_magic_link_send_validation_error(self) -> None:
        """Test for sending email magic links with validation errors."""
        try:
            req = EmailLinkSendReq(email="", redirect="", create=True)
            self.fixture.send(req)
            self.fail(msg="Expected an exception")
        except ServerException as e:
            self.assertIsNotNone(e)
            self.assertCountEqual(["email: cannot be blank", "redirect: cannot be blank"], e.get_validation_messages())

    def test_email_magic_link_send_success(self) -> None:
        """Test for sending email magic links successfully."""
        req = EmailLinkSendReq(email=TestUtils.create_random_test_email(), redirect="https://example.com", create=True)
        rsp: EmailLinkSendRsp = self.fixture.send(req)
        self.assertEqual(200, rsp.http_status_code)


class EmailMagicLinkValidateTest(TestBase):
    """Test case for validating email magic links."""

    def test_email_magic_link_validate_validation_error_empty_token(self) -> None:
        """Test for validating email magic links with empty token."""
        with self.assertRaises(expected_exception=ServerException) as context:
            req = EmailLinksValidateReq(token="")
            self.fixture.validate_email_magic_link(email_link_id="eml-123456789", req=req)

        exception: ServerException = context.exception
        self.assertCountEqual(["token: cannot be blank"], exception.get_validation_messages())

    def test_email_magic_link_validate_validation_error_invalid_id(self) -> None:
        """Test for validating email magic links with invalid ID."""
        with self.assertRaises(expected_exception=ServerException) as context:
            req = EmailLinksValidateReq(token="fdfdsfdss1fdfdsfdss1")
            self.fixture.validate_email_magic_link(email_link_id="eml-123456789", req=req)

        exception: ServerException = context.exception
        self.assertEqual(404, exception.http_status_code)
