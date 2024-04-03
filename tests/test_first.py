import unittest

from src.corbado_python_sdk.corbado_sdk import CorbadoSDK
from tests.utils import TestUtils


class TestAuthMethod(unittest.TestCase):
    print("First Test")
    assert 2 * 2 == 4


def test_square_positive_number():
    sdk: CorbadoSDK = TestUtils.instantiate_sdk()
    assert sdk is not None
