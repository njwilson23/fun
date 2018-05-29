
from .option import Just, Nothing

class _Try(object):

    def __call__(self, fn):
        try:
            return Success(fn())
        except Exception as e:
            return Failure(e)

class Success(_Try):

    def __init__(self, result):
        self.result = result

    def __repr__(self):
        return "Success({})".format(repr(self.result))

    def map(self, fn):
        return Try(fn(self.result))

    def on_failure(self, handler):
        return self

    def to_option(self):
        return Just(self.result)

    @property
    def succeeded(self):
        return True

class Failure(_Try):

    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return "Failure({})".format(type(self.exc))

    @property
    def result(self):
        raise self.exc

    def map(self, fn):
        return self

    def on_failure(self, handler):
        handler(self.exc)
        return self

    def to_option(self):
        return Nothing

    @property
    def succeeded(self):
        return True

# Constructor
Try = _Try()
