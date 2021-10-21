from typing import *

import yaml

from .constraints import *

__all__ = ["Argument", "get_arguments_from_dict"]


class Argument:
    """
    Argument Class.

    Parameters
    ----------
    name : str
        Name of the Argument.
    constraints : List[Constraint]
        List of `Constraint`.

    Attributes
    ----------
    required : bool
        Whether the argument is required (not `None`)
    default : Any
        Default value of the argument
    """

    def __init__(self, name: str, constraints: List[Constraint] = []) -> None:
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


class Validator:
    def __init__(self, dict_of_args: Dict[str, Argument]) -> None:
        self.args = dict_of_args

    def validate(self, dict_of_values: Dict[str, Any]) -> Dict[str, Any]:

        valid_args = {}
        for name, arg in self.args.items():
            if name in dict_of_values:
                assert arg(dict_of_values[name])
            else:
                assert (
                    not arg.required
                ), f"Argument `{name}` is required but not provided."
            valid_args[name] = dict_of_values[name]

        return valid_args

    def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        assert not args, "Only keyword arguments allowed for validation."
        return self.validate(kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.args})"

    @classmethod
    def from_dict(cls, dict_of_constraints: Dict[str, List[Constraint]]) -> "Validator":
        args = get_arguments_from_dict(dict_of_constraints)
        return cls(args)

    @classmethod
    def from_yaml(cls, yaml_string: str) -> "Validator":
        constraints = yaml.safe_load(yaml_string)
        return cls.from_dict(constraints)
