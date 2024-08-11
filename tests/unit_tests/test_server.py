from sway import server
from sway.config import Config


def test_get_checks_from_data(config: Config) -> None:
    response = server.get_checks_from_data(
        config, "functional_service,broken_service"
    )

    assert response[0].name == "functional_service"
    assert response[1].name == "broken_service"

    assert len(response) == 2
