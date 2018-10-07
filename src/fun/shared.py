
class Equals(object):
    """ Abstract class for defining equality between data classes """
    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.__dict__ == other.__dict__)

def identity(a):
    return a

def always(a):
    def f(*_):
        return a
    return f
