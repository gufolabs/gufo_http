# ---------------------------------------------------------------------
# Gufo HTTP: _fast typing
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from enum import Enum
from typing import Dict, Iterable, List, Optional, Tuple

# Exceptions
class HttpError(Exception):
    """Base class for Gufo HTTP errors."""

class RequestError(HttpError):
    """Request error."""

class RedirectError(HttpError):
    """Redirects limits exceeded."""

# Auth
class AuthBase(object):
    """Base class for authentication settings."""

class BasicAuth(AuthBase):
    """HTTP Basic Authentication.

    Args:
        user: User name.
        password: Optional password.
    """

    def __init__(self: "BasicAuth", user: str, password: Optional[str]) -> None: ...

class BearerAuth(AuthBase):
    def __init__(self: "BearerAuth", token: str) -> None: ...

# Request Method
class RequestMethod(Enum):
    GET: int
    HEAD: int
    OPTIONS: int
    DELETE: int
    POST: int
    PUT: int
    PATCH: int

    # def __getitem__(self: "RequestMethod", name: str) -> "RequestMethod": ...
    @staticmethod
    def get(name: str) -> Optional["RequestMethod"]: ...

# Constants for compression methods
DEFLATE: int
GZIP: int
BROTLI: int
ZSTD: int

class Headers(object):
    def __contains__(self: "Headers", k: str) -> bool: ...
    def __getitem__(self: "Headers", k: str) -> bytes: ...
    def get(self: "Headers", k: str, default: Optional[bytes]) -> Optional[bytes]: ...
    def keys(self: "Headers") -> Iterable[str]: ...
    def values(self: "Headers") -> Iterable[bytes]: ...
    def items(self: "Headers") -> Iterable[Tuple[str, bytes]]: ...

class Response(object):
    @property
    def status(self: "Response") -> int: ...
    @property
    def headers(self: "Response") -> Headers: ...
    @property
    def content(self: "Response") -> bytes: ...

class Proxy(object):
    def __init__(self: "Proxy", url: str) -> None: ...

class AsyncClient(object):
    def __init__(
        self: "AsyncClient",
        validate_cert: bool,
        connect_timeout_ns: int,
        timeout_ns: int,
        max_redirects: Optional[int],
        headers: Optional[Dict[str, bytes]],
        compression: Optional[int],
        user_agent: Optional[str],
        auth: Optional[AuthBase],
        proxy: Optional[List[Proxy]],
    ) -> None: ...
    async def request(
        self: "AsyncClient",
        method: RequestMethod,
        url: str,
        headers: Optional[Dict[str, bytes]],
        body: Optional[bytes],
    ) -> Response: ...

class SyncClient(object):
    def __init__(
        self: "SyncClient",
        validate_cert: bool,
        connect_timeout_ns: int,
        timeout_ns: int,
        max_redirects: Optional[int],
        headers: Optional[Dict[str, bytes]],
        compression: Optional[int],
        user_agent: Optional[str],
        auth: Optional[AuthBase],
        proxy: Optional[List[Proxy]],
    ) -> None: ...
    def request(
        self: "SyncClient",
        method: RequestMethod,
        url: str,
        headers: Optional[Dict[str, bytes]],
        body: Optional[bytes],
    ) -> Response: ...
