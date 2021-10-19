from typing import *

from .base import Constraint


class NOT(Constraint):
    def __init__(self, constraint) -> None:
        assert isinstance(constraint, Constraint)
        self.constraint = constraint

    def assertion(self, x: Any) -> bool:
        return not self.constraint(x)


class ANY(Constraint):
    def __init__(self, *constraints) -> None:
        for c in constraints:
            assert isinstance(c, Constraint)

        self.constraints = constraints

    def assertion(self, x: Any) -> bool:

        return any(c(x) for c in self.constraints)


class ALL(Constraint):
    def __init__(self, *constraints) -> None:
        for c in constraints:
            assert isinstance(c, Constraint)

        self.constraints = constraints

    def assertion(self, x: Any) -> bool:

        return all(c(x) for c in self.constraints)
