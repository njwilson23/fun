import copy
from functools import reduce

from .option import Just, Nothing
from .shared import always, identity, Equals, compose

# Return a function that then applied to an object replaces .key with f(obj)
def replace(key, valuef):
    def f(obj):
        new = copy.copy(obj)
        key.set_mut(new, valuef(obj))
        return new
    return f

def replace_option(key, valuef):
    return lambda optional: optional.map(replace(key, valuef))

class Attr(Equals):
    """ Representation of a class attribute that can be examined or set in-place
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return ".{}".format(self.name)

    def __call__(self, obj):
        return obj.__getattribute__(self.name)

    def get_option(self, obj):
        if hasattr(obj, self.name):
            return Just(obj.__getattribute__(self.name))
        else:
            return Nothing

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

    def get_option(self, obj):
        if self.name in obj:
            return Just(obj[self.name])
        else:
            return Nothing

    def set_mut(self, obj, value):
        obj[self.name] = value

class _Iteration(Equals):
    def __repr__(self):
        return "[...]"

    def __call__(self, obj):
        return obj

    def get_option(self, obj):
        return [Just(a) for a in obj]

    def set_mut(self, i, value):
        obj[i] = value

Iteration = _Iteration()

class Optic(Equals):
    _TYPE = "AbstractOptic"

    def __init__(self, above, key):
        self.above = above
        self.key = key

    def __repr__(self):
        return "{}({}, {})".format(self.TYPE, self.above, self.key)

    def __getitem__(self, key):
        return type(self)(Just(self), Item(key))

    def __getattr__(self, key):
        return type(self)(Just(self), Attr(key))

    def _get(self, f):
        """ _get on a root node should return a function g = f(obj) that
        applies *f* to *obj*. _get on a subnode should pass itself to the
        parent's _get method with a function wrapping logic to extract a key
        from an object at the node's level.
        """
        raise NotImplementedError

    def _set(self, f):
        """ _set is like _get, except the function passed to the parent node
        must return a copy of the object at the node's level with the key
        replaced.
        """
        raise NotImplementedError

    @property
    def for_all(self):
        return type(self)(Just(self), Iteration)

    def get(self, obj):
        return self._get(lambda a: Just(a))(obj)

    def set(self, obj, value):
        return self._set(always(Just(value)))(obj)

    def setf(self, obj, fn):
        return self._set(lambda a: Just(fn(a)))(obj)

class _Lens(Optic):
    _TYPE = "Lens"

    def _getf(self, obj, f):
        def get_and_apply(sub):
            if self.key is Iteration:
                return [f(a) for a in self.key(sub)]
            else:
                return f(self.key(sub))
        return self.above \
            .map(lambda above: above._getf(obj, get_and_apply)) \
            .otherwise(lambda: f(obj))

    def _setf(self, obj, f):
        def get_and_apply(sub):
            if self.key is Iteration:
                return [f(a) for a in self.key(sub)]
            else:
                return f(self.key(sub))
        return self.above \
            .map(lambda above: above._setf(obj, replace(self.key, get_and_apply))) \
            .otherwise(lambda: f(obj))

class _OptionLens(Optic):
    _TYPE = "OptionLens"

    def _get(self, f):
        """ produces a function that when called with a concrete obj performs a
        recursive get
        """
        # given a concrete inst, map f over the option returned at key
        def get_and_apply(inst, f):
            if self.key is Iteration:
                return [a.flat_map(f) for a in self.key.get_option(inst)]
            else:
                return self.key.get_option(inst).flat_map(f)

        # takes a concrete inst, returns an optional retrieved value
        def callback(inst):
            return get_and_apply(inst, f)

        return self.above \
            .map(lambda above: above._get(callback)) \
            .otherwise(lambda: lambda obj: f(obj))

    def _set(self, f):
        """ produces a function that when called with an object and a value
        returns a modified object set with the value.

        calling _set builds a function up the stack that passes the object to
        be modified to the root node along with a function, f. When the
        completed f is ultimately called with the object, at each stack level
        it attempts to extract the value mapping to a the local key, evaluates
        a function on the value, and returns the result.

        the final evaluation is the completely modified object.
        """

        def rcopy(obj, key):
            def fn(value):
                new = copy.copy(obj)
                key.set_mut(new, value)
                return new
            return fn

        # given a concrete inst, map f over the option returned at key
        def get_and_apply(inst, f):
            if self.key is Iteration:
                # TODO: here we need to sequence over the list of options
                return [a.flat_map(f) for a in self.key.get_option(inst)]
            else:
                return self.key.get_option(inst).flat_map(f).map(rcopy(inst, self.key))

        # takes a concrete inst, returns an optional replacement
        def callback(inst):
            replacement = get_and_apply(inst, f)
            return replacement

        return self.above \
            .map(lambda above: above._set(callback)) \
            .otherwise(lambda: lambda obj: f(obj))

Lens = _Lens(Nothing, None)
OptionLens = _OptionLens(Nothing, None)

def lens_compose(*optics):
    return reduce(lambda a, b: _Lens(Just(a), b.key), optics)

def option_lens_compose(*optics):
    return reduce(lambda a, b: _OptionLens(Just(a), b.key), optics)
