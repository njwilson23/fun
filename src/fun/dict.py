from collections import MutableMapping
from .option import Just, Nothing
from . import Try

class Dict(dict):
    """ Works just like a builtin `dict`, except get returns an Option, and
    deletion returns a Try. """

    def __init__(self, **kvs):
        self.state = {**kvs}

    def __getitem__(self, k):
        if k in self.state:
            return Just(self.state[k])
        return Nothing

    def __setitem__(self, k, v):
        self.state[k] = v

    def _del(self, k):
        del self.state[k]

    def __delitem__(self, k):
        return Try(self._del(k))
    
    def __iter__(self):
        return self.state.__iter__()

    def __len__(self):
        return len(self.state)