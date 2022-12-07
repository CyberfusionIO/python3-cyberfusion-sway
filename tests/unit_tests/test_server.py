from sway import server


def test_get_checks_from_data():
    response = server.get_checks_from_data("functional_service,broken_service")

    assert response[0].name == "functional_service"
    assert response[1].name == "broken_service"

    assert len(response) == 2
