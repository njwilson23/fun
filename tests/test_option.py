import unittest
from fun import Option, Just, Nothing

class OptionTests(unittest.TestCase):

    def test_something(self):
        something = Just("cat")
        self.assertEqual(something.extract(), "cat")

    def test_nothing(self):
        nothing = Nothing
        with self.assertRaises(ValueError):
            nothing.extract()

    def test_otherwise(self):
        something = Just("cat")
        self.assertEqual(something.otherwise("dog"), "cat")

        nothing = Nothing
        self.assertEqual(nothing.otherwise("dog"), "dog")

if __name__ == "__main__":
    unittest.main()

