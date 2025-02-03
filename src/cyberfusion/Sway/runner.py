"""Commands runner."""

import logging
import os
import subprocess
from dataclasses import dataclass
from typing import List
from tenacity import retry, stop_after_attempt, wait_fixed


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


@retry(stop=stop_after_attempt(2), wait=wait_fixed(2), reraise=True)  # type: ignore[misc]
def execute_command(command: List[str], *, timeout: int = TIMEOUT_COMMAND) -> None:
    """Execute command."""
    try:
        subprocess.check_output(
            command, stderr=subprocess.STDOUT, timeout=timeout, text=True
        )
    except subprocess.CalledProcessError as e:
        logging.warning(
            f"Failed to execute command '{command}' (RC {e.returncode}): {e.output}"
        )

        exception = CommandHasNonZeroReturnCodeError(
            command=command, return_code=e.returncode, output=e.output
        )

        raise exception from e
    except subprocess.TimeoutExpired as e:
        logging.warning(f"Failed to execute command '{command}' (timeout)")

        raise CommandTimeoutError(command=command) from e


def determine_weight() -> int:
    """Determine weight as percentage.

    Depending on the balancing `method` (such as `roundrobin`), traffic can be
    distributed over servers depending on their weight. This function determines
    weight based on system load, which is an 'accurate enough' indication of how
    busy a system is, and therefore how much traffic it can handle.

    The returned 'positive integer percentage' is "proportional to the initial
    weight of a server" (which can be set in the HAProxy config, and defaults to 1).

    The percentage does not have to be based on those of other servers, as "all
    servers will receive a load proportional to their weight relative to the sum
    of all weights, so the higher the weight, the higher the load."

    See https://docs.haproxy.org/2.6/configuration.html#5.2-agent-check and
    https://docs.haproxy.org/2.6/configuration.html#weight
    """
    load_average, _, _ = os.getloadavg()  # 1-minute load average

    # If load average is over 99, the weight percentage would either be below 1
    # or negative. Both are problematic: below 1 would cause the server to be
    # drained (default behaviour with a weight of 0, and HAProxy ignores decimals),
    # and negative values are disallowed. As a load average of over 100 is very
    # rare, and we would rarely send traffic to an overloaded server than take it
    # offline, use 99 as an upper bound.

    if load_average > 99:
        load_average = 99

    weight_percentage = (
        100 - load_average
    )  # Reverse (higher load = less traffic, lower weight percentage = less traffic)

    return int(weight_percentage)  # No decimals allowed
