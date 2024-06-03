# ---------------------------------------------------------------------
# Gufo HTTP: Python HTTP Client Library
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Gufo HTTP: The accelerated Python HTTP client library.

Attributes:
    __version__: Current version.
"""

# Gufo Labs modules
from ._fast import (
    BROTLI,
    DEFLATE,
    GZIP,
    AuthBase,
    BasicAuth,
    BearerAuth,
    Headers,
    HttpError,
    Proxy,
    RedirectError,
    RequestError,
    RequestMethod,
    Response,
)

__version__: str = "0.3.1"
__all__ = [
    "__version__",
    "HttpError",
    "RedirectError",
    "RequestError",
    "Headers",
    "DEFLATE",
    "GZIP",
    "BROTLI",
    "AuthBase",
    "BasicAuth",
    "BearerAuth",
    "RequestMethod",
    "Response",
    "Proxy",
]
