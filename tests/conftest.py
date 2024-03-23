# ---------------------------------------------------------------------
# Gufo HTTP: httpd fixture
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import logging
from typing import Iterator

# Third-party modules
import pytest

# Gufo HTTP modules
from gufo.http.httpd import Httpd, HttpdMode

from .blackhole import BlackholeHttpd
from .util import (
    HTTPD_ADDRESS,
    HTTPD_BLACKHOLE_PORT,
    HTTPD_HOST,
    HTTPD_PATH,
    HTTPD_PORT,
    HTTPD_TLS_PORT,
)


@pytest.fixture(scope="session")
def httpd() -> Iterator[Httpd]:
    logger = logging.getLogger("gufo.http.httpd")
    logger.setLevel(logging.DEBUG)
    with Httpd(
        path=HTTPD_PATH,
        address=HTTPD_ADDRESS,
        port=HTTPD_PORT,
        host=HTTPD_HOST,
    ) as httpd:
        yield httpd


@pytest.fixture(scope="session")
def httpd_tls() -> Iterator[Httpd]:
    logger = logging.getLogger("gufo.http.httpd")
    logger.setLevel(logging.DEBUG)
    with Httpd(
        path=HTTPD_PATH,
        address=HTTPD_ADDRESS,
        port=HTTPD_TLS_PORT,
        host=HTTPD_HOST,
        mode=HttpdMode.HTTPS,
    ) as httpd:
        yield httpd


@pytest.fixture(scope="session")
def httpd_blackhole() -> Iterator[BlackholeHttpd]:
    logger = logging.getLogger("gufo.http.httpd")
    logger.setLevel(logging.DEBUG)
    with BlackholeHttpd(port=HTTPD_BLACKHOLE_PORT) as httpd:
        yield httpd
