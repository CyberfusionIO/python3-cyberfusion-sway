"""Checks-related classes."""

from dataclasses import dataclass
from enum import Enum
from typing import List

from sway.runner import CommandHasNonZeroReturnCodeError, execute_command


@dataclass
class CheckNotExistsError(Exception):
    """Exception to raise when check doesn't exist."""

    name: str


class CheckStates(Enum):
    """Check states."""

    POSITIVE: str = "positive"
    NEGATIVE: str = "negative"


class Check:
    """Represents check."""

    def __init__(self, *, name: str, command: str) -> None:
        """Set attributes."""
        self.name = name
        self._command = command

        self._message = None

    @property
    def command(self) -> List[str]:
        """Get command."""
        return self._command.split(" ")

    @property
    def state(self) -> CheckStates:
        """Get state by running command."""
        try:
            execute_command(self.command)
        except CommandHasNonZeroReturnCodeError:
            return CheckStates.NEGATIVE

        return CheckStates.POSITIVE
