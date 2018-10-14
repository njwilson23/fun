
class Equals(object):
    """ Abstract class for defining equality between data classes """
    def __eq__(self, other):
        return (type(other) is type(self)) and (self.__dict__ == other.__dict__)

def identity(a):
    return a

def always(a):
    def f(*_):
        return a
    return f

def compose(fa, fb):
    return lambda a: fa(fb(a))
