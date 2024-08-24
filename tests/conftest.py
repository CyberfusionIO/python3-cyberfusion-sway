import multiprocessing
import os
import socket
from typing import Generator

import docopt
import pytest
from pytest_mock import MockerFixture

from sway import server
from sway.config import Config


@pytest.fixture
def config() -> Config:
    return Config(os.path.join("tests", "sway.yml"))


@pytest.fixture
def sway_server(mocker: MockerFixture, config: Config):
    mocker.patch(
        "sway.server.get_args",
        return_value=docopt.docopt(server.__doc__, ["--config-file-path", config.path]),
    )

    pipe_out, pipe_in = multiprocessing.Pipe()

    process = multiprocessing.Process(target=server.serve, args=(pipe_out,))
    process.start()

    pipe_in.recv()

    yield

    process.terminate()


@pytest.fixture
def sway_client_socket(
    config: Config, sway_server: Generator[None, None, None]
) -> Generator[socket.socket, None, None]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.server_host, config.server_port))

        yield s
