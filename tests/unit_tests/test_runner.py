import pytest

from cyberfusion.Sway.runner import (
    CommandHasNonZeroReturnCodeError,
    CommandTimeoutError,
    execute_command,
)
from pytest_mock import MockerFixture
from cyberfusion.Sway.runner import determine_weight


def test_execute_command_non_zero_return_code() -> None:
    with pytest.raises(CommandHasNonZeroReturnCodeError) as e:
        execute_command(["false"])

    assert e.value.command == ["false"]
    assert e.value.return_code == 1
    assert e.value.output == b""


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
