import unittest

from fun.list import List
from fun.option import Option, Something, Nothing

class ListTests(unittest.TestCase):

    def test_traverse(self):
        def effect(a):
            if a >= 0:
                return Something(a*2)
            return Nothing
        lst = List([1, 2, 3])
        traversed = lst.traverse(effect, Option)
        self.assertEqual(traversed.extract(), List([2, 4, 6]))

        lst = List([1, -2, 3])
        traversed = lst.traverse(effect, Option)
        self.assertEqual(traversed, Nothing)

    def test_empty_traverse(self):
        def effect(a):
            if a >= 0:
                return Something(a*2)
            return Nothing
        lst = List([])
        traversed = lst.traverse(effect, Option)
        self.assertEqual(traversed.extract(), List([]))

    def test_sequence(self):
        lst = List([
            Something(1),
            Something(2),
            Something(3)
        ])
        sequenced = lst.sequence(Option)
        self.assertEqual(sequenced.extract(), List([1, 2, 3]))

    def test_sequence_nothing(self):
        lst = List([
            Something(1),
            Nothing,
            Something(3)
        ])
        sequenced = lst.sequence(Option)
        self.assertEqual(sequenced, Nothing)

if __name__ == "__main__":
    unittest.main()
