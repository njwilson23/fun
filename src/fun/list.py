import functools
from collections import Sequence
from . import Try
from .shared import identity

class List(Sequence):

    def __init__(self, items):
        self.items = list(items)

    def __repr__(self):
        return "List({})".format(repr(self.items))

    def __iter__(self):
        for item in self.items:
            yield item

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return Try(lambda: self.items[index])

    def __eq__(self, other):
        if type(other) != List:
            return False
        if len(self) != len(other):
            return False
        for a, b in zip(self.items, other.items):
            if a != b:
                return False
        return True

    def __neq__(self, other):
        return not (self == other)

    @classmethod
    def append(cls, lst, item):
        return cls([*lst, item])

    def map(self, fn):
        return List(fn(a) for a in self)

    def flat_map(self, fn):
        return List(a for b in self
                      for a in fn(b))

    def traverse(self, fn, effect_type):
        """ Given a function the produces an effect from a value,

            fn(a) -> Effect(b)

        return an effect

            List(a...) -> Effect(List(b...))

        The type of the effect (e.g. Option, Try, ...) must be provided as there is
        no general way to infer it in a language like Python.
        """
        if len(self.items) == 0:
            return effect_type(List([]))

        # TODO: avoid constructing a new list on every iteration with List.append
        return functools.reduce(
            lambda a, b: a.flat_map(lambda aa: fn(b).map(lambda bb: List.append(aa, bb))),
            self.items,
            effect_type(List([]))
        )

    def sequence(self, effect_type):
        """ If list if of type List(Effect(_), Effect(_), ..., Effect(_)), return
        Effect(List(_, _, ...., _)). """
        return self.traverse(identity, effect_type)

