from typing import *


class Constraint:
    def __call__(self, x: Any):
        self.assertion(x)

    def assertion(self, x: Any) -> bool:
        raise NotImplementedError("Method `assertion` must be implemented.")

    def __repr__(self):
        return self.__class__.__name__
