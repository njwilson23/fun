import functools
from .shared import identity

class List(object):

    def __init__(self, items):
        self.items = list(items)

    def __repr__(self):
        return "List({})".format(repr(self.items))

    def __iter__(self):
        for item in self.items:
            yield item

    def __len__(self):
        return len(self.items)

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
        if len(self.items) == 0:
            return effect_type(List([]))

        effects = [fn(a) for a in self.items]
        return functools.reduce(
            lambda a, b: a.flat_map(lambda aa: b.map(lambda bb: List.append(aa, bb))),
            effects,
            effect_type(List([]))
        )

    def sequence(self, effect_type):
        return self.traverse(identity, effect_type)

