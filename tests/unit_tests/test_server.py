import os

import docopt
import pytest
import schema
from pytest_mock import MockerFixture

from sway import server
from sway.config import Config


def test_config_file_path_not_exists(mocker: MockerFixture) -> None:
    PATH = "/tmp/doesntexist"

    assert not os.path.isfile(PATH)

    mocker.patch(
        "sway.server.get_args",
        return_value=docopt.docopt(
            server.__doc__, ["--config-file-path", PATH]
        ),
    )

    with pytest.raises(
        schema.SchemaError, match="^Config file doesn't exist$"
    ):
        server.serve()


def test_get_checks_from_data(config: Config) -> None:
    response = server.get_checks_from_data(
        config, "functional_service,broken_service"
    )

    assert response[0].name == "functional_service"
    assert response[1].name == "broken_service"

    assert len(response) == 2
