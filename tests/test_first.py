import unittest


class TestAuthMethod(unittest.TestCase):
    print("First Test")
    assert 2 * 2 == 4


def test_square_positive_number():
    assert 2 * 2 == 4


if __name__ == "__main__":
    unittest.main()
