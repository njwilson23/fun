import unittest
from fun.recursion import Pure, Bind, evaluate, F

class RecursionTests(unittest.TestCase):

    def test_construction_dsl(self):
        output = evaluate(
            Bind(lambda s: F.pure(s + " world"), Pure("hello"))
        )
        self.assertEqual("hello world", output)

    def test_construction(self):
        output = F.pure("hello").map(lambda s: s + " world").evaluate()
        self.assertEqual("hello world", output)

    def test_deep_recursion(self):
        def sum_to(acc):
            def f(n):
                if n <= 0: return F.pure(acc)
                else: return F.pure(n - 1).bind(sum_to(acc + n))
            return f

        result = F.pure(10000).bind(sum_to(0)).evaluate()
        self.assertEqual(50005000, result)

if __name__ == "__main__":
    unittest.main()
