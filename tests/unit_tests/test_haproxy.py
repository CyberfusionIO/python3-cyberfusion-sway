from cyberfusion.Sway.config import Config
from cyberfusion.Sway.haproxy import HAProxyStateWord, Response


def test_response_negative_state_checks(config: Config) -> None:
    negative_state_checks = Response(checks=config.checks)._negative_state_checks

    assert len(negative_state_checks) == 1

    assert negative_state_checks[0].name == "broken_service"


def test_response_description_down(config: Config) -> None:
    assert (
        Response(checks=config.checks).description
        == "# The following checks have a negative state: broken_service"
    )


def test_response_description_up(config: Config) -> None:
    assert Response(checks=[config.checks[0]]).description is None


def test_response_string_down(config: Config) -> None:
    assert (
        str(Response(checks=config.checks))
        == "down # The following checks have a negative state: broken_service\n"
    )


def test_response_string_up(config: Config) -> None:
    assert str(Response(checks=[config.checks[0]])) == "up\n"


def test_response_state_down(config: Config) -> None:
    state = Response(checks=config.checks).state

    assert state == HAProxyStateWord.DOWN


def test_response_state_up(config: Config) -> None:
    state = Response(checks=[config.checks[0]]).state

    assert state == HAProxyStateWord.UP
