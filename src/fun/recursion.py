import dataclasses
from typing import Any, Callable, Generic, Tuple, TypeVar

T = TypeVar('T')
U = TypeVar('U')

class F(Generic[T]):
    @staticmethod
    def value(a: T) -> 'F[T]':
        return Value(a)

    def bind(self, func: Callable[[Any], 'F[U]']) -> 'F[U]':
        return Bind(func, self)

    def map(self, func: Callable[[T], U]) -> 'F[U]':
        """ Equivalent to self.bind(compose(F.value, func)) """
        return Bind(lambda a: Value(func(a)), self)

    def evaluate(self) -> T:
        return evaluate(self)

    @staticmethod
    def flatten(func: Callable[[T], 'F[U]'], arg: 'F[T]') -> 'F[U]':
        """ Equivalent to arg.bind(func) """
        return Bind(func, arg)

    @staticmethod
    def apply(func: Callable[[T], 'F[U]'], arg: T) -> 'F[U]':
        """ Equivalent to F.Value(arg).map(func) """
        return Bind(func, Value(arg))

@dataclasses.dataclass
class Value(F[T]):
    value: T

@dataclasses.dataclass
class Bind(F[U], Generic[T, U]):
    func: Callable[[T], F[U]]
    over: F[T]

def evaluate(program):
    current = program
    while isinstance(current, F):
        if isinstance(current, Value):
            return current.value
        elif isinstance(current, Bind):
            current = current.func(evaluate(current.over))
            continue
    raise TypeError
