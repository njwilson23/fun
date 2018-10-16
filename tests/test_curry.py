import unittest

from fun.shared import curry

class CurryTests(unittest.TestCase):

    def test_args(self):
        def f(a, b, c):
            return (a, b, c)

        g = curry(f)
        self.assertEqual(g(1)("b")(["three"]), (1, "b", ["three"]))

    def test_no_args(self):
        def f():
            return 1

        g = curry(f)
        self.assertEqual(g(), 1)

    def test_kwargs(self):
        def f(a = 1, b = 2):
            return a + b

        g = curry(f)
        self.assertEqual(g()(3), 4)

if __name__ == "__main__":
    unittest.main()
