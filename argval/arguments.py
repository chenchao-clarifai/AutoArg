from typing import *

from .constraints import *

__all__ = ["Argument", "get_arguments_from_dict"]


class Argument:
    def __init__(self, name: str, constraints: List[Constraint] = []):
        self.name = name
        self.required = Required() in constraints
        self.default = None
        for c in constraints:
            assert isinstance(c, Constraint)
            if not self.required and isinstance(c, Default):
                self.default = c.value

        self.constraints = constraints

    def __call__(self, x: Any) -> bool:

        return all(c(x) for c in self.constraints)

    def __repr__(self) -> str:
        return f"Argument(name={self.name}, "
        f"constraints={self.constraints})"

    def __eq__(self, other: "Argument"):
        return self.__dict__ == other.__dict__


def get_arguments_from_dict(
    d: Dict[str, List[Union[str, Constraint]]]
) -> Dict[str, Argument]:
    def _str_to_py_obj(x):
        if isinstance(x, str):
            return eval(x)
        return x

    out = {}
    for name, constraints in d.items():
        constraints = [_str_to_py_obj(c) for c in constraints]
        out[name] = Argument(name=name, constraints=constraints)

    return out
