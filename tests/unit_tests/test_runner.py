import pytest

from sway.runner import (
    CommandHasNonZeroReturnCodeError,
    CommandTimeoutError,
    execute_command,
)


def test_execute_command_non_zero_return_code():
    with pytest.raises(CommandHasNonZeroReturnCodeError) as e:
        execute_command(["false"])

    assert e.value.command == ["false"]
    assert e.value.return_code == 1
    assert e.value.output == b""


def test_execute_command_timeout():
    with pytest.raises(CommandTimeoutError) as e:
        execute_command(["sleep", "5"], timeout=1)

    assert e.value.command == ["sleep", "5"]
