import unittest

from fun.option import Option, Something, Nothing

class OptionTests(unittest.TestCase):

    def test_something(self):
        something = Something("cat")
        self.assertEqual(something.extract(), "cat")

    def test_nothing(self):
        nothing = Nothing
        with self.assertRaises(ValueError):
            nothing.extract()

    def test_otherwise(self):
        something = Something("cat")
        self.assertEqual(something.otherwise("dog").extract(), "cat")

        nothing = Nothing
        self.assertEqual(nothing.otherwise("dog").extract(), "dog")

if __name__ == "__main__":
    unittest.main()

