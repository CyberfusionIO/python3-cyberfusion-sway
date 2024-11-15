import socket
from typing import Generator

from pytest_mock import MockerFixture


def test_check_weight(
    sway_client_socket: Generator[socket.socket, None, None], mocker: MockerFixture
) -> None:
    mocker.patch("cyberfusion.Sway.haproxy.determine_weight", return_value=1)

    sway_client_socket.sendall(b"\n")

    data = sway_client_socket.recv(1024).decode("utf-8")

    assert "%" in data
    assert data.split("%")[0][-1].isdigit()


def test_check_positive_state(
    sway_client_socket: Generator[socket.socket, None, None],
) -> None:
    sway_client_socket.sendall(b"functional_service\n")

    data = sway_client_socket.recv(1024).decode("utf-8")

    assert "up" in data.split()


def test_check_negative_state(
    sway_client_socket: Generator[socket.socket, None, None],
) -> None:
    sway_client_socket.sendall(b"broken_service\n")

    data = sway_client_socket.recv(1024).decode("utf-8")

    assert "down # The following checks have a negative state: broken_service" in data
