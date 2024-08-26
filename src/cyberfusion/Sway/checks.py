"""Checks-related classes."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Union

from cyberfusion.Sway.runner import execute_command


@dataclass
class CheckNotExistsError(Exception):
    """Check doesn't exist."""

    name: str


class CheckState(Enum):
    """Check states."""

    POSITIVE: str = "positive"
    NEGATIVE: str = "negative"


class Check:
    """Represents check."""

    def __init__(self, *, name: str, command: Union[str, list]) -> None:
        """Set attributes."""
        self.name = name
        self._command = command

        self._message = None

    @property
    def command(self) -> List[str]:
        """Get command."""
        if not isinstance(self._command, list):
            return self._command.split(" ")

        return self._command

    @property
    def state(self) -> CheckState:
        """Get state by running command."""
        try:
            execute_command(self.command)
        except Exception:
            return CheckState.NEGATIVE

        return CheckState.POSITIVE
