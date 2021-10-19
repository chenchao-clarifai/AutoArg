from pathvalidate import is_valid_filepath

from .base import Constraint, IsInstance


class IsString(IsInstance):
    def __init__(self) -> None:
        super().__init__(str)


class ValidPath(Constraint):
    def __init__(self, platform="linux") -> None:
        assert platform in ("windows", "linux", "macos", "posix", "universal")
        self.platform = platform

    def assertion(self, x: str):
        return is_valid_filepath(x, platform=self.platform)

    def __repr__(self):
        return f"{super().__repr__()}(platform={self.platform})"
