# ---------------------------------------------------------------------
# Gufo HTTP: Test utilities
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import contextlib
import os
import random
import select
import socket
from logging import getLogger
from threading import Thread
from types import TracebackType
from typing import Dict, Optional, Type

HTTPD_PATH = "/usr/sbin/nginx"
HTTPD_HOST = "local.gufolabs.com"
HTTPD_ADDRESS = "127.0.0.1"
HTTPD_PORT = random.randint(52000, 53999)
HTTPD_TLS_PORT = random.randint(52000, 53999)
HTTPD_BLACKHOLE_PORT = random.randint(52000, 53999)
UNROUTABLE_URL = "http://192.0.2.1/"
UNROUTABLE_PROXY = "http://192.0.2.1:3128/"
TEXT_PLAIN = "text/plain"

logger = getLogger("gufo.httpd.httpd")


@contextlib.contextmanager
def with_env(env: Dict[str, str]) -> None:
    """
    Temporary setup environment variables.

    Set up environment variables during context
    and restore previous state on exit.
    """
    # Store state
    _prev = {k: os.environ.get(k) for k in env}
    # Setup
    for k, v in env.items():
        os.environ[k] = v
    # Return control into context
    yield
    # Restore
    for k, v in _prev.items():
        if v is None and k in os.environ:
            del os.environ[k]
        elif v is not None:
            os.environ[k] = v


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
