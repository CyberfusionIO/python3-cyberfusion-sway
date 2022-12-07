"""TCP server."""

import logging
import socket
from multiprocessing.connection import Connection
from typing import List, Optional

from sway.checks import Check, CheckNotExistsError
from sway.config import Config
from sway.haproxy import Response
from sway.runner import TIMEOUT_COMMAND

TIMEOUT_SOCKET = TIMEOUT_COMMAND + 1

ENABLED_SYSTEMD = True

try:
    import sdnotify
    from systemd.journal import JournalHandler
except ImportError:
    ENABLED_SYSTEMD = False

root_logger = logging.getLogger()
root_logger.propagate = False
root_logger.setLevel(logging.DEBUG)

if ENABLED_SYSTEMD:
    root_logger.addHandler(JournalHandler())

logger = logging.getLogger(__name__)


config = Config()


def get_checks_from_data(data: str) -> List[Check]:
    """Get checks objects from TCP request data."""
    return [
        config.get_check_by_name(name=check_name)
        for check_name in data.split(",")
    ]


def serve(
    multiprocessing_connection: Optional[Connection] = None,  # For tests
) -> None:
    """Serve TCP requests."""
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # Don't wait for TIME_WAIT expire
        server_socket.bind((config.server_host, config.server_port))
        server_socket.listen(config.server_max_connections)

        if ENABLED_SYSTEMD:
            sdnotify.SystemdNotifier().notify("READY=1")

        if multiprocessing_connection:
            multiprocessing_connection.send("Ready")

        while True:
            try:
                client_socket, client_address = server_socket.accept()

                with client_socket:
                    client_socket.settimeout(TIMEOUT_SOCKET)

                    logger.info(f"{client_address} Established connection")

                    data = client_socket.recv(1024).decode("utf-8").rstrip()

                    response = str(Response(checks=get_checks_from_data(data)))

                    logger.info(
                        f"{client_address} Sending back response '{response.rstrip()}'..."
                    )
                    client_socket.sendall(response.encode("utf-8"))
            except CheckNotExistsError:
                logger.warning(
                    f"{client_address} Requested non-existent check, not sending back response"
                )
            except socket.timeout:
                logger.warning(
                    f"{client_address} Did not receive data in {TIMEOUT_SOCKET} seconds"
                )
