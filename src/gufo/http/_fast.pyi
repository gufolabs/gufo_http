# ---------------------------------------------------------------------
# Gufo HTTP: _fast typing
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from typing import Dict, Iterable, Optional, Tuple

class HttpError(Exception): ...
class RequestError(HttpError): ...
class ConnectError(HttpError): ...
class RedirectError(HttpError): ...
class AlreadyReadError(HttpError): ...

# Constants for request methods
GET: int
HEAD: int
OPTIONS: int
DELETE: int
POST: int
PUT: int
PATCH: int

# Constants for compression methods
DEFLATE: int
GZIP: int
BROTLI: int

class Headers(object):
    def __contains__(self: "Headers", k: str) -> bool: ...
    def __getitem__(self: "Headers", k: str) -> bytes: ...
    def get(
        self: "Headers", k: str, default: Optional[bytes]
    ) -> Optional[bytes]: ...
    def keys(self: "Headers") -> Iterable[str]: ...
    def values(self: "Headers") -> Iterable[bytes]: ...
    def items(self: "Headers") -> Iterable[Tuple[str, bytes]]: ...

class AsyncResponse(object):
    @property
    def status(self: "AsyncResponse") -> int: ...
    @property
    def headers(self: "AsyncResponse") -> Headers: ...
    async def read(self: "AsyncResponse") -> bytes: ...

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
    ) -> None: ...
    async def request(
        self: "AsyncClient",
        method: int,
        url: str,
        headers: Optional[Dict[str, bytes]],
        body: Optional[bytes],
    ) -> AsyncResponse: ...
