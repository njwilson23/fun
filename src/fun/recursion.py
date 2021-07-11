import dataclasses
from typing import Any, Callable

# For type signatures
class _F: pass

class F:
    @staticmethod
    def pure(a: Any) -> _F:
        return Pure(a)

    def bind(self, func: Callable[[Any], _F]) -> _F:
        return Bind(func, self)

    def map(self, func: Callable[[Any], Any]) -> _F:
        """ Equivalent to self.bind(compose(F.pure, func)) """
        return Bind(lambda a: Pure(func(a)), self)

    def evaluate(self) -> Any:
        return evaluate(self)

    @staticmethod
    def flatten(func: Callable[[Any], _F], arg: Any):
        """ Equivalent to arg.bind(func) """
        return Bind(func, arg)

    @staticmethod
    def apply(func: Callable[[Any], _F], arg: Any):
        """ Equivalent to F.pure(arg).map(func) """
        return Bind(func, Pure(arg))

@dataclasses.dataclass
class Pure(F):
    value: Any

@dataclasses.dataclass
class Bind(F):
    func: Callable[[Any], F]
    over: F

def evaluate(program):
    current = program
    while isinstance(current, F):
        if isinstance(current, Pure):
            return current.value
        elif isinstance(current, Bind):
            current = current.func(evaluate(current.over))
            continue
    raise TypeError
