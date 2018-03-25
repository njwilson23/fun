import unittest

from fun.attempt import Try, Success, Failure

class TryTests(unittest.TestCase):

    def test_success(self):
        result = Try(lambda: 1+2)
        self.assertEqual(result.result, 3)

    def test_failure(self):
        result = Try(lambda: 1/0)
        with self.assertRaises(ZeroDivisionError):
            result.result

if __name__ == "__main__":
    unittest.main()
