from cyberfusion.Sway.checks import CheckState
from cyberfusion.Sway.config import Config


def test_check_command_string(config: Config) -> None:
    assert config.get_check_by_name(name="multiple_words_command").command == [
        "echo",
        "hello",
    ]


def test_check_command_list(config: Config) -> None:
    assert config.get_check_by_name(name="multiple_items_command").command == [
        "echo",
        "hello",
    ]


def test_check_state_positive(config: Config) -> None:
    assert (
        config.get_check_by_name(name="functional_service").state == CheckState.POSITIVE
    )


def test_check_state_negative(config: Config) -> None:
    assert config.get_check_by_name(name="broken_service").state == CheckState.NEGATIVE
