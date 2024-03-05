# ---------------------------------------------------------------------
# Gufo HTTP: Python HTTP Client Library
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Gufo HTTP: The accelerated Python HTTP client library.

Attributes:
    __version__: Current version
"""

# Gufo Labs modules
from ._fast import (
    BROTLI,
    DEFLATE,
    GZIP,
    AlreadyReadError,
    AuthBase,
    BasicAuth,
    BearerAuth,
    ConnectError,
    Headers,
    HttpError,
    RedirectError,
    RequestError,
)

__version__: str = "0.1.1"
__all__ = [
    "__version__",
    "HttpError",
    "RedirectError",
    "RequestError",
    "ConnectError",
    "AlreadyReadError",
    "Headers",
    "DEFLATE",
    "GZIP",
    "BROTLI",
    "AuthBase",
    "BasicAuth",
    "BearerAuth",
]
