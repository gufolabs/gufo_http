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
from gufo.http.httpd import Httpd
from .util import HTTPD_PATH, HTTPD_HOST, HTTPD_ADDRESS, HTTPD_PORT


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
