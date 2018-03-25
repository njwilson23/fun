import unittest

from fun.option import Option, Something, Nothing

class OptionTests(unittest.TestCase):

    def test_something(self):
        something = Something("cat")
        self.assertEqual(something.get(), "cat")
        self.assertEqual(something.get_or_else("dog"), "cat")

    def test_nothing(self):
        nothing = Nothing
        with self.assertRaises(ValueError):
            nothing.get()
        self.assertEqual(nothing.get_or_else("dog"), "dog")

if __name__ == "__main__":
    unittest.main()

