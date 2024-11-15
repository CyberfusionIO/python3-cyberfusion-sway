"""HAProxy-related classes."""

from enum import Enum
from typing import List, Optional

from cyberfusion.Sway.checks import Check, CheckState
from cyberfusion.Sway.runner import determine_weight


class HAProxyStateWord(Enum):
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
            if check.state != CheckState.NEGATIVE:
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
    def state(self) -> HAProxyStateWord:
        """Get state."""
        if self._negative_state_checks:
            return HAProxyStateWord.DOWN

        return HAProxyStateWord.UP

    @property
    def weight(self) -> str:
        """Get weight."""
        return str(determine_weight()) + "%"

    def __str__(self) -> str:
        """Stringify response."""
        result = []

        result.append(self.weight)
        result.append(self.state.value)

        if self.description is not None:
            result.append(self.description)

        return " ".join(result)
