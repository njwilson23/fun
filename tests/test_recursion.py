import unittest
from fun.recursion import Value, Bind, evaluate, F

class RecursionTests(unittest.TestCase):

    def test_construction_dsl(self):
        output = evaluate(
            Bind(lambda s: F.value(s + " world"), Value("hello"))
        )
        self.assertEqual("hello world", output)

    def test_construction(self):
        output = F.value("hello").map(lambda s: s + " world").evaluate()
        self.assertEqual("hello world", output)

    def test_deep_recursion(self):
        def sum_to(acc):
            def f(n):
                if n <= 0: return F.value(acc)
                else: return F.value(n - 1).bind(sum_to(acc + n))
            return f

        result = F.value(10000).bind(sum_to(0)).evaluate()
        self.assertEqual(50005000, result)

if __name__ == "__main__":
    unittest.main()
