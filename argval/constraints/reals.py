from .base import Constraint


class IsFloat(Constraint):
    def assertion(self, x: float):

        assert isinstance(x, float)
