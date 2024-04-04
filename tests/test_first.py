import unittest

from corbado_python_sdk.corbado_sdk import CorbadoSDK
from tests.utils import TestUtils


class TestAuthMethod(unittest.TestCase):
    print("First Test")
    assert 2 * 2 == 4

    def test_instantiate_sdk(self) -> None:
        print("success")
        sdk: CorbadoSDK = TestUtils.instantiate_sdk()
        self.assertIsNotNone(obj=sdk)


def test_instantiate_sdk() -> None:
    print("success")
    sdk: CorbadoSDK = TestUtils.instantiate_sdk()
    assert sdk is not None


# def test_user_list(self):
#   sdk: CorbadoSDK = TestUtils.instantiate_sdk()
