# ---------------------------------------------------------------------
# Gufo HTTP: Public types declaration
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""Public types declaration."""
# Python modules
from enum import IntEnum

# Gufo HTTP modules
from ._fast import DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT


class RequestMethod(IntEnum):
    """
    Request method.

    Attributes:
        GET: HTTP GET request.
        HEAD: HTTP HEAD request.
        OPTIONS: HTTP OPTIONS request.
        DELETE: HTTP DELETE request.
        POST: HTTP POST request.
        PUT: HTTP PUT request.
        PATCH: HTTP PATCH request.
    """

    GET = GET
    HEAD = HEAD
    OPTIONS = OPTIONS
    DELETE = DELETE
    POST = POST
    PUT = PUT
    PATCH = PATCH
