from typing import *

from .constraint import Constraint


class Argument:
    def __init__(
        self, name: str, type: Union[Any, Tuple[Any]], constraints: List[Constraint]
    ):
        self.name = name
        self.type = type
        for c in constraints:
            assert isinstance(c, Constraint)
        self.constraints = constraints

    def __call__(self, x: Any) -> bool:

        if not isinstance(x, self.type):
            return False

        return all(c(x) for c in self.constraints)

    def __repr__(self) -> str:
        return f"Argument(name={self.name}, type={self.type}, constraints={self.constraints}"
