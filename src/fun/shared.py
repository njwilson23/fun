import inspect

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

def curry(fn):
    sig = inspect.signature(fn)

    def buildfn(f, args):
        if len(args) < 2:
            g = f
        elif args[0].default is inspect.Parameter.empty:
            def g(a):
                return buildfn(lambda *rest: f(a, *rest), args[1:])
        else:
            def g(a=args[0].default):
                return buildfn(lambda *rest: f(a, *rest), args[1:])
        return g

    return buildfn(fn, tuple(sig.parameters.values()))
