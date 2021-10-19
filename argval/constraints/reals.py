from .base import IsInstance


class IsFloat(IsInstance):
    def __init__(self):
        super().__init__(self, float)


class IsInteger(IsInstance):
    def __init__(self):
        super().__init__(self, int)


class IsReal(IsInstance):
    def __init__(self):
        super().__init__(self, (int, float))


# class InRange(Constraint):
#
#     def
