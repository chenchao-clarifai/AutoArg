from typing import *

from .base import Constraint


class Required(Constraint):
    def assertion(self, x: Any) -> bool:

        if x is None:  # required arg cannot be null
            return False

        return True


class Default(Constraint):
    """Default: Pass default value to `Argument` class.
    No constraint imposed.

    Parameters
    ----------
    default_value : Any
        The default value for the argument

    Attributes
    ----------
    value : Any
        The default value

    """

    def __init__(self, default_value: Any):
        self.value = default_value

    def assertion(self, x: Any):

        # no constraints
        return True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(default_value={self.value})"
