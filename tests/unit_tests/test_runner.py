import pytest

from cyberfusion.Sway.runner import (
    CommandHasNonZeroReturnCodeError,
    CommandTimeoutError,
    execute_command,
)
from pytest_mock import MockerFixture
from cyberfusion.Sway.runner import determine_weight
import logging
from _pytest.logging import LogCaptureFixture


def test_execute_command_non_zero_return_code(caplog: LogCaptureFixture) -> None:
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(CommandHasNonZeroReturnCodeError) as e:
            execute_command(["touch"])

    assert e.value.command == ["touch"]
    assert e.value.return_code == 1
    assert e.value.output

    assert (
        f"Failed to execute command '{e.value.command}' (RC {e.value.return_code}): {e.value.output}"
        in caplog.text
    )


def test_execute_command_timeout() -> None:
    with pytest.raises(CommandTimeoutError) as e:
        execute_command(["sleep", "5"], timeout=1)

    assert e.value.command == ["sleep", "5"]


def test_determine_weight_upper_bound(mocker: MockerFixture) -> None:
    mocker.patch("os.getloadavg", return_value=(100.0, 100.0, 100.0))

    assert determine_weight() == 1


def test_determine_weight(mocker: MockerFixture) -> None:
    mocker.patch("os.getloadavg", return_value=(3.0, 2.0, 1.0))

    assert determine_weight() == 97
