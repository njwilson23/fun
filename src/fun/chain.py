from abc import ABC
from .option import Just, Nothing

class _BaseChain(ABC):

    def prepend(self, a):
        return _Pair(_Single(a), self)

    def append(self, a):
        return _Pair(self, _Single(a))

    def __iter__(self):
        rest = self
        while True:
            maybe, rest = rest.split_head()
            if maybe.is_defined:
                yield maybe.extract()
            else:
                break

    def __eq__(self, other):
        if not isinstance(other, _BaseChain):
            return False
        for (this, that) in zip(self, other):
            if this != that:
                return False
        return True

class _Empty(_BaseChain):
    def headOption(self):
        return Nothing

    def lastOption(self):
        return Nothing

    def prepend(self, a):
        return _Single(a)

    def append(self, a):
        return _Single(a)

    def split_head(self):
        return (Nothing, Empty)

    def split_last(self):
        return (Empty, Nothing)

    def is_empty(self):
        return True

class _Single(_BaseChain):
    def __init__(self, a):
        self._a = a

    def headOption(self):
        return Just(self._a)

    def lastOption(self):
        return Just(self._a)

    def split_head(self):
        return (Just(self._a), Empty)

    def split_last(self):
        return (Empty, Just(self._a))

    def is_empty(self):
        return False

class _Pair(_BaseChain):
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def headOption(self):
        return self._left.headOption

    def lastOption(self):
        return self._right.headOption

    def split_head(self):
        left_head, left_tail = self._left.split_head()
        return (left_head, _Pair(left_tail, self._right))

    def split_last(self):
        right_pre, right_last= self._right.split_last()
        return (_Pair(self._right, right_pre), right_last)

    def is_empty(self):
        return False

class _Wrap(_BaseChain):
    def __init__(self, seq):
        self._seq = seq

    def headOption(self):
        if len(self._seq) == 0:
            return Nothing
        else:
            return Just(self._seq[0])

    def lastOption(self):
        if len(self._seq) == 0:
            return Nothing
        else:
            return Just(self._seq[-1])

    def split_head(self):
        if len(self._seq) == 0:
            return (Nothing, Empty)
        elif len(self._seq) == 1:
            return (Just(self._seq[0]), Empty)
        else:
            return (Just(self._seq[0]), _Wrap(self._seq[1:]))

    def split_last(self):
        if len(self._seq) == 0:
            return (Empty, Nothing)
        elif len(self._seq) == 1:
            return (Empty, Just(self._seq[0]))
        else:
            return (_Wrap(self._seq[:-1]), Just(self._seq[-1]))

    def is_empty(self):
        return len(self._seq) == 0

Empty = _Empty()

# Constructor for a chain variant, misleadingly made to look like a class
def Chain(seq=None):
    if seq is None:
        return Empty
    elif hasattr(seq, "__iter__"):
        return _Wrap(seq)
    else:
        return _Single(seq)
