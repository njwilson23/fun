
class Option(object):
    pass

class Something(Option):
    def __init__(self, value):
        self.value = value

    def map(self, fn):
        return Something(fn(self.value))

    def flat_map(self, fn):
        result = fn(self.value)
        if isinstance(result, Option):
            return result
        else:
            raise TypeError(f"expected Option, not {type(result)}")
        return fn(self.value)

    def get(self):
        return self.value

    def get_or_else(self, alternative):
        return self.get()

class _Nothing(Option):
    def __init__(self):
        pass

    def map(self, fn):
        return Nothing

    def flat_map(self, fn):
        return Nothing

    def get(self):
        raise ValueError("undefined")

    def get_or_else(self, alternative):
        return alternative

Nothing = _Nothing()
