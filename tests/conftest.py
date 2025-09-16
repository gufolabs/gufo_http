# ---------------------------------------------------------------------
# Gufo HTTP: httpd fixture
# ---------------------------------------------------------------------
# Copyright (C) 2024-25, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import logging
import socket
from typing import Iterator

# Third-party modules
import pytest

# Gufo HTTP modules
from gufo.http.httpd import Httpd, HttpdMode

from .blackhole import BlackholeHttpd
from .proxy import ProxyServer
from .util import (
    HTTPD_ADDRESS,
    HTTPD_HOST,
)


def get_free_port() -> int:
    """Get free TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))  # Bind to a random available port
        return sock.getsockname()[1]  # Get assigned port


@pytest.fixture(scope="session")
def httpd() -> Iterator[Httpd]:
    logger = logging.getLogger("gufo.http.httpd")
    logger.setLevel(logging.DEBUG)
    with Httpd(
        address=HTTPD_ADDRESS,
        port=get_free_port(),
        host=HTTPD_HOST,
    ) as httpd:
        yield httpd


@pytest.fixture(scope="session")
def httpd_tls() -> Iterator[Httpd]:
    logger = logging.getLogger("gufo.http.httpd")
    logger.setLevel(logging.DEBUG)
    with Httpd(
        address=HTTPD_ADDRESS,
        port=get_free_port(),
        host=HTTPD_HOST,
        mode=HttpdMode.HTTPS,
    ) as httpd:
        yield httpd


@pytest.fixture(scope="session")
def httpd_blackhole() -> Iterator[BlackholeHttpd]:
    logger = logging.getLogger("gufo.http.httpd")
    logger.setLevel(logging.DEBUG)
    with BlackholeHttpd(port=get_free_port()) as httpd:
        yield httpd


@pytest.fixture(scope="session")
def proxy() -> Iterator[ProxyServer]:
    logger = logging.getLogger("gufo.http.httpd")
    logger.setLevel(logging.DEBUG)
    with ProxyServer(port=get_free_port()) as proxy:
        yield proxy
