"""Checks-related classes."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Union

from sway.runner import execute_command


@dataclass
class CheckNotExistsError(Exception):
    """Exception to raise when check doesn't exist."""

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
