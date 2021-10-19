from .base import IsInstance


class IsFloat(IsInstance):
    def __init__(self):
        super().__init__(float)


class IsInteger(IsInstance):
    def __init__(self):
        super().__init__(int)


class IsReal(IsInstance):
    def __init__(self):
        super().__init__((int, float))


# class InRange(Constraint):
#
#     def
