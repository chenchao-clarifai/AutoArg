from enum import Enum
from typing import *

from .operators import Operator

__all__ = ["Filter", "NormalMode"]


class NormalMode(Enum):
    WHITE = "normal_white"  # normal white: grey -> white
    BLACK = "normal_black"  # normal white: grey -> black


class Filter(Operator):
    """
    Filter base class.

    Parameters
    ----------
    dict_of_bool : Dict[str, bool]
        Dictionary of `bool` variables indicating whether the filter keeps
        (`True`) or removes (`False`) the keyword variable.
    mode : Union[str, NormalMode]
        The mode of filter is the default treatment of unspecified grey variables.

    Attributes
    ----------
    mode : Union[str, NormalMode]
        The mode of filter is the default treatment of unspecified grey variables.
    """

    def __init__(
        self,
        dict_of_bool: Dict[str, bool],
        mode: Union[str, NormalMode] = "normal_white",
    ) -> None:
        super().__init__(dict_of_bool)
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
