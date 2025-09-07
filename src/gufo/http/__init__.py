# ---------------------------------------------------------------------
# Gufo HTTP: Python HTTP Client Library
# ---------------------------------------------------------------------
# Copyright (C) 2024-25, Gufo Labs
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

__version__: str = "0.5.0"
__all__ = [
    "BROTLI",
    "DEFLATE",
    "GZIP",
    "AuthBase",
    "BasicAuth",
    "BearerAuth",
    "Headers",
    "HttpError",
    "Proxy",
    "RedirectError",
    "RequestError",
    "RequestMethod",
    "Response",
    "__version__",
]
