import unittest
from fun import Try, Success, Failure

class TryTests(unittest.TestCase):

    def test_success(self):
        result = Try(lambda: 1+2)
        self.assertEqual(result.result, 3)

    def test_failure(self):
        result = Try(lambda: 1/0)
        with self.assertRaises(ZeroDivisionError):
            result.result

    def test_args(self):

        def f(a, b, c=1):
            return a + b - c

        result = Try(f, 2, 4, c=5)
        self.assertEqual(result.result, 1)

    def test_on_failure(self):
        result = Try(lambda: 1/0)\
                    .map_failure(KeyError, lambda exc: "a")\
                    .map_failure(ZeroDivisionError, lambda exc: "b")

        self.assertEqual(result.result, "b")

if __name__ == "__main__":
    unittest.main()
