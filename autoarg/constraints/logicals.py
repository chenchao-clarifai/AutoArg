from typing import *

from .base import Constraint, IsInstance

__all__ = ["IsBool", "NOT", "ANY", "ALL"]


class IsBool(IsInstance):
    def __init__(self):
        super().__init__(bool)


class NOT(Constraint):
    def __init__(self, constraint: Constraint) -> None:
        assert isinstance(constraint, Constraint)
        self.constraint = constraint

    def assertion(self, x: Any) -> bool:
        return not self.constraint(x)


class ANY(Constraint):
    def __init__(self, *constraints: Constraint) -> None:
        for c in constraints:
            assert isinstance(c, Constraint)

        self.constraints = constraints

    def assertion(self, x: Any) -> bool:

        return any(c(x) for c in self.constraints)


class ALL(Constraint):
    def __init__(self, *constraints: Constraint) -> None:
        for c in constraints:
            assert isinstance(c, Constraint)

        self.constraints = constraints

    def assertion(self, x: Any) -> bool:

        return all(c(x) for c in self.constraints)
