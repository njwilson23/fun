import copy
from functools import reduce

from .option import Just, Nothing
from .shared import always, identity, Equals

# Return a function that then applied to an object replaces .key with f(obj)
def replace(key, valuef):
    def f(obj):
        new = copy.copy(obj)
        key.set_mut(new, valuef(obj))
        return new
    return f

class Attr(Equals):
    """ Representation of a class attribute that can be examined or set in-place
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return ".{}".format(self.name)

    def __call__(self, obj):
        return obj.__getattribute__(self.name)

    def set_mut(self, obj, value):
        obj.__setattr__(self.name, value)

class Item(Equals):
    """ Representation of a dict item that can be examined or set in-place
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "[{}]".format(self.name)

    def __call__(self, obj):
        return obj.__getitem__(self.name)

    def set_mut(self, obj, value):
        obj[self.name] = value

class _Lens(object):

    def __init__(self, above, key):
        self.above = above
        self.key = key

    def __repr__(self):
        return "Lens({}, {})".format(self.above, self.key)

    def __eq__(self, other):
        return (self.key == other.key) and (self.above == other.above)

    def __getitem__(self, key):
        return _Lens(Just(self), Item(key))

    def __getattr__(self, key):
        return _Lens(Just(self), Attr(key))

    def _getf(self, obj, f):
        def get_and_apply(sub):
            return f(self.key(sub))
        return self.above \
            .map(lambda above: above._getf(obj, get_and_apply)) \
            .otherwise(lambda: f(obj))

    def _setf(self, obj, f):
        def get_and_apply(sub):
            return f(self.key(sub))
        return self.above \
            .map(lambda above: above._setf(obj, replace(self.key, get_and_apply))) \
            .otherwise(lambda: f(obj))

    def get(self, obj):
        return self._getf(obj, identity)

    def set(self, obj, value):
        return self._setf(obj, always(value))

Lens = _Lens(Nothing, None)

# class Prism(object):

def compose_optics(*optics):
    return reduce(lambda a, b: _Lens(Just(a), b.key), optics)
