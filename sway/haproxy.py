"""HAProxy-related classes."""

from enum import Enum
from typing import List, Optional

from sway.checks import Check, CheckStates


class HAProxyStateWords(Enum):
    """HAProxy states.

    From https://cbonte.github.io/haproxy-dconv/2.4/configuration.html#5.2-agent-check
    """

    READY: str = "ready"
    DRAIN: str = "drain"
    MAINT: str = "maint"
    DOWN: str = "down"
    FAIL: str = "fail"
    STOPPED: str = "stopped"
    UP: str = "up"


class Response:
    """Represents response to HAProxy agent check."""

    CHAR_SHARP = "#"

    def __init__(self, *, checks: List[Check]) -> None:
        """Set attributes."""
        self.checks = checks

    @property
    def _negative_state_checks(self) -> List[Check]:
        """Get checks with negative state."""
        result = []

        for check in self.checks:
            if check.state != CheckStates.NEGATIVE:
                continue

            result.append(check)

        return result

    @property
    def description(self) -> Optional[str]:
        """Get description."""
        if not self._negative_state_checks:
            return None

        words = [
            self.CHAR_SHARP,
            "The following checks have a negative state:",
        ]

        for check in self._negative_state_checks:
            words.append(check.name)

        return " ".join(words)

    @property
    def state(self) -> HAProxyStateWords:
        """Get state."""
        if self._negative_state_checks:
            return HAProxyStateWords.DOWN

        return HAProxyStateWords.UP

    def __str__(self) -> str:
        """Stringify response."""
        if self.description is not None:
            return f"{self.state.value} {self.description}\n"

        return f"{self.state.value}\n"
