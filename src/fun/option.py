
class _Option(object):

    def __call__(self, value):
        return Just(value)

class Just(_Option):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Just({})".format(repr(self.value))

    def map(self, fn):
        return Just(fn(self.value))

    def flat_map(self, fn):
        result = fn(self.value)
        if isinstance(result, _Option):
            return result
        else:
            raise TypeError(f"expected Option, not {type(result)}")
        return fn(self.value)

    def otherwise(self, value):
        return self

    def extract(self):
        return self.value

class _Nothing(_Option):

    def __init__(self):
        pass

    def __repr__(self):
        return "Nothing"

    def map(self, fn):
        return Nothing

    def flat_map(self, fn):
        return Nothing

    def otherwise(self, value):
        return Just(value)

    def extract(self):
        raise ValueError("cannot extract value from Nothing")

Option = _Option()
Nothing = _Nothing()