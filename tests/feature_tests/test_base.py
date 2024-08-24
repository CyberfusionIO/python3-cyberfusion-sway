import socket
from typing import Generator


def test_check_positive_state(
    sway_client_socket: Generator[socket.socket, None, None],
) -> None:
    sway_client_socket.sendall(b"functional_service\n")

    data = sway_client_socket.recv(1024).decode("utf-8")

    assert data == "up\n"


def test_check_negative_state(
    sway_client_socket: Generator[socket.socket, None, None],
) -> None:
    sway_client_socket.sendall(b"broken_service\n")

    data = sway_client_socket.recv(1024).decode("utf-8")

    assert data == "down # The following checks have a negative state: broken_service\n"
