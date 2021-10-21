from typing import *

from .base import Constraint


class Required(Constraint):
    def assertion(self, x: Any) -> bool:

        if x is None:  # required arg cannot be null
            return False

        return True
