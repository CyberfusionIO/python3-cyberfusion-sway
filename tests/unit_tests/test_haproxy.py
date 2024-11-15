from pytest_mock import MockerFixture

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
    string = str(Response(checks=config.checks))

    assert "down" in string.split()
    assert "The following checks have a negative state: broken_service" in string


def test_response_string_up(config: Config) -> None:
    string = str(Response(checks=[config.checks[0]]))

    assert "up" in string.split()


def test_response_string_weight(config: Config, mocker: MockerFixture) -> None:
    mocker.patch("cyberfusion.Sway.haproxy.determine_weight", return_value=1)

    string = str(Response(checks=[]))

    assert "1%" in string.split()


def test_response_state_down(config: Config) -> None:
    state = Response(checks=config.checks).state

    assert state == HAProxyStateWord.DOWN


def test_response_state_up(config: Config) -> None:
    state = Response(checks=[config.checks[0]]).state

    assert state == HAProxyStateWord.UP


def test_response_weight(config: Config) -> None:
    weight = Response(checks=[]).weight

    assert weight
