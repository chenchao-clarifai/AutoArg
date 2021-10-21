import string
from typing import *

import yaml

from .constraints import *

__all__ = ["Argument", "Validator"]


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
        return f"Argument(name={self.name}, constraints={self.constraints})"

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


class Operator:
    def __init__(self, dict_of_x: Dict[str, Any]) -> None:
        self.args = dict_of_x

    def operate(self, dict_of_values: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Method `operate` must be implemented.")

    def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        assert not args, "Only keyword arguments allowed for validation."
        return self.operate(kwargs)

    def __eq__(self, other) -> bool:
        assert isinstance(other, self.__class__)
        return self.args == other.args

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.args})"

    @classmethod
    def from_dict(cls, dict_of_x: Dict[str, List[Constraint]]) -> "Operator":
        raise NotImplementedError("Class Method `from_dict` must be implemented.")

    @classmethod
    def from_yaml(cls, yaml_string: str) -> "Operator":
        init = yaml.safe_load(yaml_string)
        return cls.from_dict(init)


class Validator(Operator):
    """Validator validates a dictionary of values using a dictionary of
    `Argument`s."""

    def __init__(self, dict_of_args: Dict[str, Argument]) -> None:
        super().__init__(dict_of_args)

    def operate(self, dict_of_values: Dict[str, Any]) -> Dict[str, Any]:
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

    @classmethod
    def from_dict(cls, dict_of_constraints: Dict[str, List[Constraint]]) -> "Validator":
        args = get_arguments_from_dict(dict_of_constraints)
        return cls(args)


class Converter(Operator):
    """Converter converts a dictionary of argument values to another dictionary
    of argument values."""

    def __init__(self, dict_of_template_strings: Dict[str, str]) -> None:
        super().__init__(dict_of_template_strings)

    def operate(self, dict_of_values: Dict[str, Any]) -> Dict[str, Any]:
        dict_of_str = {k: str(v) for k, v in dict_of_values.items()}
        new = {}
        for name, eqn in self.args.items():
            template = string.Template(eqn)
            eqn = template.substitute(dict_of_str)
            try:
                new[name] = eval(eqn)
            except NameError:
                new[name] = eqn

        return new

    @classmethod
    def from_dict(
        cls, dict_of_template_strings: Dict[str, List[Constraint]]
    ) -> "Converter":
        return cls(dict_of_template_strings)
