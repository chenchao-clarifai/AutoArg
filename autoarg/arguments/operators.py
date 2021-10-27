import string
from typing import *

import yaml

from ..constraints import *
from .argument import *

__all__ = ["Validator", "Converter"]


class Operator:
    """
    Operator base class.

    Parameters
    ----------
    dict_of_any : Dict[str, Any]
        Map from string names to objects of Any type.

    Attributes
    ----------
    args : Dict[str, Any]
        Map from string names to objects of Any type.
    """

    def __init__(self, dict_of_any: Dict[str, Any]) -> None:
        self.args = dict_of_any

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

    def __len__(self) -> int:
        return len(self.args)

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
                assert arg(
                    dict_of_values[name]
                ), f"Value {name} = {dict_of_values[name]} is not compatible with {str(arg)}."
                valid_args[name] = dict_of_values[name]
            else:
                assert (
                    not arg.required
                ), f"Argument `{name}` is required but not provided."
                valid_args[name] = arg.default

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
            except Exception:
                new[name] = eqn

        return new

    @classmethod
    def from_dict(
        cls, dict_of_template_strings: Dict[str, List[Constraint]]
    ) -> "Converter":
        return cls(dict_of_template_strings)
