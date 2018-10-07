def identity(a):
    return a

def always(a):
    def f(*_):
        return a
    return f
