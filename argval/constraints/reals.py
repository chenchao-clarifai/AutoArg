from typing import *

from .base import Constraint, IsInstance


class IsFloat(IsInstance):
    def __init__(self):
        super().__init__(float)


class IsInteger(IsInstance):
    def __init__(self):
        super().__init__(int)


class IsReal(IsInstance):
    def __init__(self):
        super().__init__((int, float))


class InRange(Constraint):
    """
    Assert the number is in *union* of the provided ranges. The ranges should be
    str and with format.

    [ or (
    lower bound
    ,
    upper bound
    ] or )

    separated by *single space*

    You may use 'inf', 'oo' to represent infinity
    and '-inf' or '-oo' to represent negative infinity

    e.g. '( 0.1 , 100 ]', '[ -1 , oo )'


    Parameters
    ----------
    *ranges : str
        A series of string representation of intervals.

    Attributes
    ----------
    ranges : List[str]
        List of string representation of intervals
    rules : List[Callable]
        List of bool functions;
        each function returns `True` if the arg is within
        the corresponding interval
    """

    _map_infs = {
        "oo": float("inf"),
        "+oo": float("inf"),
        "inf": float("inf"),
        "+inf": float("inf"),
        "-oo": -float("inf"),
        "-inf": -float("inf"),
    }

    def __init__(self, *ranges: str):
        assert isinstance(ranges, tuple)
        self.ranges = ranges
        self.rules = [self._parse_eq(r) for r in self.ranges]

    def assertion(self, x: Union[int, float]) -> bool:

        assert isinstance(x, (int, float))

        return any(r(x) for r in self.rules)

    def __repr__(self) -> str:
        return f"{super().__repr__()}({', '.join(self.ranges)})"

    def _parse_eq(self, eq: str) -> Callable:

        assert isinstance(eq, str)
        eq_ = eq.split(" ")

        # [ or ( ... lower_bound ... , ... upper_bound ... ) or ]
        # 0 ........ 1 ............. 2 ... 3 ............. 4

        assert len(eq_) == 5
        assert eq_[0] in ("[", "(")
        assert eq_[4] in ("]", ")")
        assert eq_[2] == ","

        if eq_[1] in self._map_infs:
            lower_bound = self._map_infs[eq_[1]]
        else:
            lower_bound = float(eq_[1])

        if eq_[3] in self._map_infs:
            upper_bound = self._map_infs[eq_[3]]
        else:
            upper_bound = float(eq_[3])

        if eq_[0] == "[":

            def left_rule(x):
                return x >= lower_bound

        else:  # '('

            def left_rule(x):
                return x > lower_bound

        if eq_[4] == "]":

            def right_rule(x):
                return x <= upper_bound

        else:  # ')'

            def right_rule(x):
                return x < upper_bound

        def rule(x):
            return left_rule(x) and right_rule(x)

        return rule


class Positive(InRange):
    def __init__(self):
        super().__init__("( 0 , oo )")


class Negative(InRange):
    def __init__(self):
        super().__init__("( -oo , 0 )")


class NonNegative(InRange):
    def __init__(self):
        super().__init__("[ 0 , oo )")


class NonPositive(InRange):
    def __init__(self):
        super().__init__("( -oo , 0 ]")
