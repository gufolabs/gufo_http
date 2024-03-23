# ---------------------------------------------------------------------
# Gufo HTTP: Blackhole HTTP server
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import select
import socket
from logging import getLogger
from threading import Thread
from types import TracebackType
from typing import Optional, Type

logger = getLogger("gufo.httpd.httpd")


class BlackholeHttpd(object):
    """Blackhole server to test request timeouts."""

    def __init__(
        self: "BlackholeHttpd",
        address: str = "127.0.0.1",
        port: int = 10000,
        host: str = "local.gufolabs.com",
    ) -> None:
        self._address = address
        self._port = port
        self._host = host
        self.prefix = f"http://{self._host}:{self._port}"
        self._thread: Optional[Thread] = None
        self._to_shutdown = False

    def __enter__(self: "BlackholeHttpd") -> "BlackholeHttpd":
        """Context manager entry."""
        self.start()
        return self

    def __exit__(
        self: "BlackholeHttpd",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Context manager exit."""
        self.stop()

    def start(self: "BlackholeHttpd") -> None:
        """Start server."""
        self._thread = Thread(name=f"blackhole-{self._port}", target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def stop(self: "BlackholeHttpd") -> None:
        """Stop server."""
        self._to_shutdown = True
        if self._thread:
            self._thread.join(3.0)
            self._thread = None

    def _run(self: "BlackholeHttpd") -> None:
        """Server implementation."""
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        readers = [listener]
        listener.bind((self._address, self._port))
        listener.listen(5)
        logger.info("Listeninng %s:%s", self._address, self._port)
        while not self._to_shutdown:
            readers, _, _ = select.select(readers, [], [], 1.0)
            for sock in readers:
                if sock == listener:
                    # New connection
                    new_client, remote_addr = listener.accept()
                    logger.info("Connect from %s", remote_addr)
                    readers.append(new_client)
                else:
                    # Incoming data
                    data = sock.recv(1024)
                    if data:
                        logger.info("Received: %s", data)
                    else:
                        # Connection closed
                        logger.info("Connnnection closed")
                        sock.close()
                        readers.remove(sock)
