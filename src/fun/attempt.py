
class _Try(object):

    def __call__(self, fn):
        try:
            return Success(fn())
        except Exception as e:
            return Failure(e)

class Success(_Try):

    def __init__(self, result):
        self.value = result

    def __str__(self):
        return "Success({})".format(self.value)

    def map(self, fn):
        return Try(fn(self.value))

class Failure(_Try):

    def __init__(self, exc):
        self.exc = exc

    def __str__(self):
        return "Failure({})".format(type(self.exc))

    @property
    def value(self):
        raise self.exc

    def map(self, fn):
        return self

# Constructor
Try = _Try()
