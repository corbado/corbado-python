# type: ignore
import os
import unittest
from time import time
from unittest.mock import AsyncMock, MagicMock, patch

from jwt import encode
from pydantic import ValidationError

from corbado_python_sdk import Config, CorbadoSDK, SessionValidationResult
from corbado_python_sdk.services import SessionService

TEST_NAME = "Test Name"
TEST_EMAIL = "test@email.com"
TEST_PHONE_NUMBER = "+012345678"
TEST_USER_ID = "12345"


class TestBase(unittest.TestCase):
    """Base class for all test using mocking for SessionService.

    Args:
        unittest (_type_): unittest

    Raises:
        FileNotFoundError: If no private key was found

    """

    mock_urlopen = None

    @classmethod
    def setUpClass(cls) -> None:
        # Setup, read private key and jwks for mocking
        cls.session_service: SessionService = cls.create_session_service()

        jwks_path: str = os.path.join(os.path.dirname(__file__), "test_data", "jwks.json")
        try:
            with open(file=jwks_path, mode="rb") as private_key_file:
                cls.jwks: bytes = private_key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Failed to read private key file")

    def setUp(self) -> None:
        self.my_patch = patch("urllib.request.urlopen")
        self.mock_urlopen: MagicMock | AsyncMock = self.my_patch.start()
        self.addCleanup(self.my_patch.stop)
        # Mock the response
        self.mock_response = MagicMock()
        self.mock_response.__enter__.return_value = self.mock_response
        self.mock_response.read.return_value = self.jwks
        self.mock_urlopen.return_value = self.mock_response

    @classmethod
    def create_session_service(cls) -> SessionService:
        """Create test configuration of SessionService.

        Warning! You should normally use SessionService from CorbadoSDK for non-test purposes.

        Returns:
            SessionService: SessionService instance
        """
        return SessionService(
            issuer="https://auth.acme.com",
            jwks_uri="https://example_uri.com",  # does not matter, url access is mocked
            short_session_cookie_name="cbo_short_session",
        )

    def tearDown(self) -> None:
        self.my_patch.stop()

    def _provide_jwts(self):
        """Provide list of jwts with expected test results."""
        return [
            # JWT with invalid format
            (False, "invalid"),
            # JWT signed with wrong algorithm (HS256 instead of RS256)
            (
                False,
                """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6
                IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.dyt0CoTl4WoVjAHI9Q_CwSKhl6d_9rhM3NrXuJttkao""",
            ),
            # Not before (nfb) in future
            (False, self._generate_jwt(iss="https://auth.acme.com", exp=int(time()) + 100, nbf=int(time()) + 100)),
            # Expired (exp)
            (False, self._generate_jwt(iss="https://auth.acme.com", exp=int(time()) - 100, nbf=int(time()) - 100)),
            # Invalid issuer (iss)
            (False, self._generate_jwt(iss="https://invalid.com", exp=int(time()) + 100, nbf=int(time()) - 100)),
            # Success
            (True, self._generate_jwt(iss="https://auth.acme.com", exp=int(time()) + 100, nbf=int(time()) - 100)),
        ]

    @classmethod
    def _generate_jwt(cls, iss: str, exp: int, nbf: int) -> str:
        payload = {
            "iss": iss,
            "iat": int(time()),
            "exp": exp,
            "nbf": nbf,
            "sub": TEST_USER_ID,
            "name": TEST_NAME,
        }

        private_key_path: str = os.path.join(os.path.dirname(__file__), "test_data", "privateKey.pem")
        try:
            with open(file=private_key_path, mode="rb") as private_key_file:
                private_key = private_key_file.read()
        except FileNotFoundError:
            raise FileNotFoundError("Failed to read private key file")

        return encode(payload, private_key, algorithm="RS256", headers={"kid": "kid123"})


class TestSessionService(TestBase):
    def test_get_and_validate_short_session_value(self):
        for valid, token in self._provide_jwts():
            result: SessionValidationResult = self.session_service.get_and_validate_short_session_value(
                short_session=token
            )

            self.assertEqual(first=valid, second=result.authenticated)
            self.assertEqual(first=valid, second=result.error is None)

            if valid:
                self.assertEqual(first=TEST_NAME, second=result.full_name)
                self.assertEqual(TEST_USER_ID, result.user_id)

    def test_cache_jwk_set_used_expect_reduced_urlopen_calls(self):
        jwt: str = self._generate_jwt(iss="https://auth.acme.com", exp=int(time()) + 100, nbf=int(time()) - 100)
        self.session_service.get_and_validate_short_session_value(short_session=jwt)
        num_calls: int = self.mock_urlopen.call_count
        for _i in range(3):
            self.session_service.get_and_validate_short_session_value(short_session=jwt)
        self.assertEqual(num_calls, self.mock_urlopen.call_count)

    def test_generate_jwt(self):
        iss = "issuer"
        exp = 1234567890  # Example expiration time
        nbf = 0  # Example not-before time

        jwt_token: str = self._generate_jwt(iss=iss, exp=exp, nbf=nbf)
        self.assertIsNotNone(jwt_token)

    def test_init_parameters(self):
        test_cases = [
            # Valid session service
            ({"issuer": "s", "jwks_uri": "2", "short_session_cookie_name": "name"}, True),
            # Test empty issuer
            ({"issuer": "", "jwks_uri": "2", "short_session_cookie_name": "name"}, False),
            # Test empty jwks_uri
            ({"issuer": "s", "jwks_uri": "", "short_session_cookie_name": "name"}, False),
            # Tesft empty short_session_cookie_name
            ({"issuer": "s", "jwks_uri": "2", "short_session_cookie_name": ""}, False),
        ]

        for params, expected_result in test_cases:
            if expected_result:
                # No exception should be raised
                assert isinstance(SessionService(**params), SessionService)
            else:
                # ValidationError should be raised
                with self.assertRaises(ValidationError):
                    SessionService(**params)


class TestSessionServiceConfiguration(TestBase):
    def test_set_cname_expect_issuer_changed(self):
        test_cname = "cname.test.com"
        config: Config = Config(api_secret="corbado1_XXX", project_id="pro-55", cname=test_cname)
        sdk = CorbadoSDK(config=config)
        sessions: SessionService = sdk.sessions
        self.assertEqual("https://" + test_cname, sessions.issuer)
