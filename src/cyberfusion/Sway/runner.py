"""Commands runner."""

import subprocess
from dataclasses import dataclass
from typing import List

TIMEOUT_COMMAND = 1


@dataclass
class CommandHasNonZeroReturnCodeError(Exception):
    """Command has non-zero return code."""

    command: List[str]
    return_code: int
    output: str


@dataclass
class CommandTimeoutError(Exception):
    """Command timed out."""

    command: List[str]


def execute_command(command: List[str], *, timeout: int = TIMEOUT_COMMAND) -> None:
    """Execute command."""
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.CalledProcessError as e:
        raise CommandHasNonZeroReturnCodeError(
            command=command, return_code=e.returncode, output=e.output
        ) from e
    except subprocess.TimeoutExpired as e:
        raise CommandTimeoutError(command=command) from e
