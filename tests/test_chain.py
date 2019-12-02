import unittest

from fun.chain import Empty, _Single, _Pair, _Wrap, Chain

class ChainTests(unittest.TestCase):

    def test_eqality(self):
        # no matter how implemented, chains that iterate the same are equal
        one = _Pair(_Single("a"), _Single("b"))
        two = _Wrap(("a", "b"))
        three = Empty.append("b").prepend("a")
        self.assertEqual(one, two)
        self.assertEqual(one, three)

        # but standard Python collections can't play
        self.assertNotEqual(one, ["a", "b"])
        self.assertNotEqual(one, ("a", "b"))

    def test_append(self):
        inputs = [
                Empty,
                _Single(1),
                _Pair(_Single(1), _Wrap([2, 3, 4])),
                _Wrap([1, 2, 3])
        ]

        appended = [a.append(9) for a in inputs]
        expected = [
                Chain(9),
                Chain([1, 9]),
                Chain([1, 2, 3, 4, 9]),
                Chain([1, 2, 3, 9])
        ]

        for (wanted, actual) in zip(expected, appended):
            self.assertEqual(wanted, actual)

    def test_prepend(self):
        inputs = [
                Empty,
                _Single(1),
                _Pair(_Single(1), _Wrap([2, 3, 4])),
                _Wrap([1, 2, 3])
        ]

        prepended = [a.prepend(0) for a in inputs]
        expected = [
                Chain(0),
                Chain([0, 1]),
                Chain([0, 1, 2, 3, 4]),
                Chain([0, 1, 2, 3])
        ]

        for (wanted, actual) in zip(expected, prepended):
            self.assertEqual(wanted, actual)

    def test_iteration(self):
        chain = _Pair(
                _Wrap([1, 2, 3]),
                _Pair(_Single(4), _Wrap([5, 6, 7]))
        )

        expected = range(1, 8)
        for wanted, actual in zip(expected, chain):
            self.assertEqual(wanted, actual)


if __name__ == "__main__":
    unittest.main()
