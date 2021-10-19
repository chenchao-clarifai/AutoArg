from typing import *

from .constraints import *


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


def get_arguments_from_dict(d: Dict[str, Dict[str, str]]) -> Dict[str, Argument]:

    out = {}
    for k, v in d.items():
        v["name"] = k
        v["type"] = eval(v["type"])
        v["constraints"] = [eval(c) for c in v["constraints"]]
        out[k] = Argument(**v)

    return out
