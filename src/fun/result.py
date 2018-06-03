
from .option import Just, Nothing

class _Result(object):

    def __call__(self, fn, *args, **kwargs):
        try:
            return Success(fn(*args, **kwargs))
        except Exception as e:
            return Failure(e)

class Success(_Result):

    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return "Success({})".format(repr(self.result))

    def map(self, fn):
        return Try(fn(self.result))

    def flat_map(self, fn):
        return fn(self.result)

    def map_failure(self, etype, handler):
        return self

    def on_failure(self, handler):
        return self

    def to_option(self):
        return Just(self.result)

    @property
    def succeeded(self):
        return True

    def isa(self, etype):
        return False

class Failure(_Result):

    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return "Failure({})".format(type(self.exc))

    @property
    def result(self):
        raise self.exc

    def map(self, fn):
        return self

    def flat_map(self, fn):
        return self

    def map_failure(self, etype, handler):
        if isinstance(self.exc, etype):
            return Try(handler, self.exc)
        else:
            return self

    def on_failure(self, handler):
        handler(self.exc)
        return self

    def to_option(self):
        return Nothing

    @property
    def succeeded(self):
        return False

    def isa(self, etype):
        return isinstance(self.exc, etype)

# Constructor
Try = _Result()
