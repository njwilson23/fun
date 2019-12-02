
class _Option(object):

    def __call__(self, value):
        return Just(value)

class Just(_Option):

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Just) and self.value == other.value

    def __repr__(self):
        return "Just({})".format(repr(self.value))

    def map(self, fn):
        return Just(fn(self.value))

    def flat_map(self, fn):
        result = fn(self.value)
        if isinstance(result, _Option):
            return result
        else:
            raise TypeError("expected Option, not {}".format(type(result)))
        return fn(self.value)

    def otherwise(self, fn):
        return self.value

    def extract(self):
        return self.value

    def extract_or_else(self, const):
        return self.value

    @property
    def is_defined(self):
        return True

class _Nothing(_Option):

    def __init__(self):
        pass

    def __eq__(self, other):
        return other is Nothing

    def __repr__(self):
        return "Nothing"

    def map(self, fn):
        return Nothing

    def flat_map(self, fn):
        return Nothing

    def otherwise(self, fn):
        return fn()

    def extract(self):
        raise ValueError("cannot extract value from Nothing")

    def extract_or_else(self, const):
        return const

    @property
    def is_defined(self):
        return False

Option = _Option()
Nothing = _Nothing()

def unit(a):
    return Just(a)

def sequence(lst):
    # shitty implementation
    result = []
    for item in lst:
        if item is Nothing:
            return Nothing
        else:
            result.append(item.extract())
    return Just(result)
