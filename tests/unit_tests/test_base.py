import socket
from typing import Generator


def test_newline(
    sway_client_socket: Generator[socket.socket, None, None],
) -> None:
    sway_client_socket.sendall(b"\n")

    data = sway_client_socket.recv(1024).decode("utf-8")

    assert data.endswith("\n")
