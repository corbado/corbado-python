import unittest

from corbado_python_sdk import CorbadoSDK
from corbado_python_sdk.exceptions import ServerException
from corbado_python_sdk.generated.models import AuthTokenValidateReq
from corbado_python_sdk.services.interface import AuthTokenInterface
from tests.utils import TestUtils


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        cls.fixture: AuthTokenInterface = cls.sdk.auth_token_interface


class AuthTokenValidateTest(TestBase):
    """
    Test case for validating authentication tokens.

    This class contains test methods for validating different scenarios of authentication tokens.

    """

    def test_auth_token_validate_validation_error_empty_token(self) -> None:
        """
        Test case for validating authentication token with empty token.

        """
        with self.assertRaises(expected_exception=ServerException) as context:
            req = AuthTokenValidateReq(
                token="",
                clientInfo=self.sdk.create_client_info(remote_address="124.0.0.1", user_agent="IntegrationTest"),
            )

            self.fixture.validate_auth_token(req)

        exception: ServerException = context.exception
        self.assertIsNotNone(exception)
        self.assertCountEqual(["token: cannot be blank"], exception.get_validation_messages())

    def test_auth_token_validate_validation_error_invalid_token(self) -> None:
        """
        Test case for validating authentication token with invalid token.

        """
        with self.assertRaises(expected_exception=ServerException) as context:
            req = AuthTokenValidateReq(
                token="x",
                clientInfo=self.sdk.create_client_info(remote_address="124.0.0.1", user_agent="IntegrationTest"),
            )
            self.fixture.validate_auth_token(req)

        exception: ServerException = context.exception
        self.assertIsNotNone(exception)

        self.assertCountEqual(["token: the length must be exactly 64"], exception.get_validation_messages())

    def test_auth_token_validate_validation_error_not_existing_token(self) -> None:
        """
        Test case for validating non-existing authentication token.

        """
        with self.assertRaises(expected_exception=ServerException) as context:
            req = AuthTokenValidateReq(
                token=TestUtils.generate_string(characters="qwertyuiasdghj", length=64),
                clientInfo=self.sdk.create_client_info(remote_address="124.0.0.1", user_agent="IntegrationTest"),
            )
            self.fixture.validate_auth_token(req)

        exception: ServerException = context.exception

        self.assertIsNotNone(exception)
        self.assertEqual(404, exception.http_status_code)
