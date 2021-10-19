from typing import *


class Constraint:
    def __call__(self, x: Any):
        self.assertion(x)

    def assertion(self, x: Any) -> bool:
        raise NotImplementedError("Method `assertion` must be implemented.")

    def __repr__(self):
        return self.__class__.__name__


class IsInstance(Constraint):
    def __init__(self, instance_cls: Union[Any, Tuple[Any]]) -> None:

        self.instance_cls = instance_cls

    def assertion(self, x: Any) -> bool:
        return True if isinstance(x, self.instance_cls) else False
