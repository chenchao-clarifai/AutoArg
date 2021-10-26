import json

import yaml
from pathvalidate import is_valid_filepath

from .base import Constraint, IsInstance

__all__ = ["IsString", "ValidPath", "ValidJson", "ValidYaml"]


class IsString(IsInstance):
    def __init__(self) -> None:
        super().__init__(str)


class ValidPath(Constraint):
    def __init__(self, platform="linux") -> None:
        assert platform in ("windows", "linux", "macos", "posix", "universal")
        self.platform = platform

    def assertion(self, x: str) -> bool:
        return is_valid_filepath(x, platform=self.platform)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(platform={self.platform})"


class ValidJson(Constraint):
    def assertion(self, x: str) -> bool:
        try:
            json.loads(x)
            return True
        except json.JSONDecodeError:
            return False


class ValidYaml(Constraint):
    def assertion(self, x: str) -> bool:
        try:
            yaml.safe_load(x)
            return True
        except yaml.scanner.ScannerError:
            return False
