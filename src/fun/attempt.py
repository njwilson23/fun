
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

# Constructor
Try = _Try()
