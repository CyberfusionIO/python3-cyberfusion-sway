import multiprocessing
import os
import socket
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from pytest_mock import MockerFixture

from sway import server
from sway.config import Config


@pytest.fixture
def config() -> Config:
    return Config()


@pytest.fixture(autouse=True)
def config_file_path_mock(mocker: MockerFixture, request: SubRequest) -> None:
    if "original_config_file_path" in request.keywords:
        return

    mocker.patch(
        "sway.config.get_config_file_path",
        return_value=os.path.join("tests", "sway.yml"),
    )


@pytest.fixture
def sway_server():
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
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
        s.connect(("::1", config.server_port))

        yield s
