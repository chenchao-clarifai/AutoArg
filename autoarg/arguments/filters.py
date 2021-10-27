from enum import Enum
from typing import *

from .operators import Operator

__all__ = ["Filter", "NormalMode", "BlackList", "WhiteList"]


class NormalMode(Enum):
    WHITE = "normal_white"  # normal white: grey -> white
    BLACK = "normal_black"  # normal white: grey -> black

    @staticmethod
    def opposite_mode(mode: "NormalMode") -> "NormalMode":

        assert isinstance(mode, NormalMode), "The `mode` must be a `NormalMode`"

        if mode == NormalMode.WHITE:
            return NormalMode.BLACK

        if mode == NormalMode.BLACK:
            return NormalMode.WHITE


def _union_of_keys(x: Dict[str, Any], y: Dict[str, Any]) -> Set[str]:
    x_keys = set(x.keys())
    y_keys = set(y.keys())
    return x_keys.union(y_keys)


def _fill_dict_with_const(
    x: Dict[str, Any], keys: Set[str], value: Any
) -> Dict[str, Any]:
    y = {}
    for key in keys:
        if key in x:
            y[key] = x[key]
        else:
            y[key] = value
    return y


def _mode_to_bool(mode: NormalMode) -> bool:
    if mode == NormalMode.WHITE:
        return True
    elif mode == NormalMode.BLACK:
        return False
    else:
        raise ValueError(f"Input `mode` must be an `NormalMode` but get {mode}.")


class Filter(Operator):
    """
    Filter base class.

    Parameters
    ----------
    specs : Dict[str, bool]
        Dictionary of `bool` variables indicating whether the filter keeps
        (`True`) or removes (`False`) the keyword variable.
    mode : Union[str, NormalMode]
        The mode of filter is the default treatment of unspecified grey variables.

    Attributes
    ----------
    args : Dict[str, bool]
        Dictionary of `bool` variables indicating whether the filter keeps
        (`True`) or removes (`False`) the keyword variable.
    mode : Union[str, NormalMode]
        The mode of filter is the default treatment of unspecified grey variables.
    """

    def __init__(
        self,
        specs: Dict[str, bool],
        mode: Union[str, NormalMode] = "normal_white",
    ) -> None:
        super().__init__(specs)
        if isinstance(mode, str):
            mode = NormalMode(mode)
        self.mode = mode

    def operate(self, dict_of_values: Dict[str, Any]) -> Dict[str, Any]:

        filtered_values = {}
        for name, value in dict_of_values.items():
            if name in self.args:
                if self.args[name]:
                    filtered_values[name] = value
            else:  # grey variable
                if self.mode == NormalMode.WHITE:
                    # normal white: grey -> white
                    filtered_values[name] = value

        return filtered_values

    @classmethod
    def from_dict(cls, dict_of_init_kwargs: Dict[str, Any]) -> "Filter":
        return cls(**dict_of_init_kwargs)

    def __eq__(self, other: "Filter") -> bool:
        _, self_args, other_args = self._binary_op_util(other)
        return (
            isinstance(other, Filter)
            and self_args == other_args
            and self.mode == other.mode
        )

    def _binary_op_util(
        self, other: "Filter"
    ) -> Tuple[Set[str], Dict[str, Any], Dict[str, Any]]:
        assert isinstance(other, Filter), "Other must be a `Filter`"
        keys = _union_of_keys(self.args, other.args)
        self_args = _fill_dict_with_const(self.args, keys, _mode_to_bool(self.mode))
        other_args = _fill_dict_with_const(other.args, keys, _mode_to_bool(other.mode))

        return keys, self_args, other_args

    def __and__(self, other: "Filter") -> "Filter":

        keys, self_args, other_args = self._binary_op_util(other)

        new_args = {}
        for key in keys:
            new_args[key] = self_args[key] and other_args[key]

        if _mode_to_bool(self.mode) and _mode_to_bool(other.mode):
            new_mode = "normal_white"
        else:
            new_mode = "normal_black"
        return Filter(new_args, new_mode)

    def __or__(self, other: "Filter") -> "Filter":
        keys, self_args, other_args = self._binary_op_util(other)
        new_args = {}
        for key in keys:
            new_args[key] = self_args[key] or other_args[key]

        if _mode_to_bool(self.mode) or _mode_to_bool(other.mode):
            new_mode = "normal_white"
        else:
            new_mode = "normal_black"
        return Filter(new_args, new_mode)

    def __invert__(self) -> "Filter":
        new_args = {}
        for name, value in self.args.items():
            new_args[name] = not value
        mode = NormalMode.opposite_mode(self.mode)
        return Filter(new_args, mode)


class BlackList(Filter):
    """BlackList Filter removes all variables within the `black_list` and keeps
    all other unspecified variables."""

    def __init__(self, black_list: List[str]) -> None:
        bools = {name: False for name in black_list}
        mode = NormalMode.WHITE
        super().__init__(bools, mode)


class WhiteList(Filter):
    """WhiteList Filter keeps all variables within the `white_list` and removes
    all other variables."""

    def __init__(self, white_list: List[str]) -> None:
        bools = {name: True for name in white_list}
        mode = NormalMode.BLACK
        super().__init__(bools, mode)
