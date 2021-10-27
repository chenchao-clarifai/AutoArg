from typing import *

__all__ = ["Constraint", "IsInstance"]


class Constraint:
    def __call__(self, x: Any) -> bool:
        return self.assertion(x)

    def assertion(self, x: Any) -> bool:
        raise NotImplementedError("Method `assertion` must be implemented.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__


class IsInstance(Constraint):
    def __init__(self, instance_cls: Union[Any, Tuple[Any]]) -> None:
        self.instance_cls = instance_cls

    def assertion(self, x: Any) -> bool:
        return isinstance(x, self.instance_cls)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.instance_cls})"
