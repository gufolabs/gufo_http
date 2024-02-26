# ---------------------------------------------------------------------
# Gufo HTTP: HttpClient implementation
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Asynchronous client."""

# Python modules
from types import TracebackType
from typing import AsyncIterator, Dict, Iterable, Optional, Tuple, Type, Union


# Gufo HTTP modules
from ._fast import AsyncClient, AsyncResponse

MAX_REDIRECTS = 10


class HttpClient(object):
    """
    Asynchronous HTTP client.

    Args:
        max_redirects: Maximal amount of redirects. Use `None`
            to disable redirect processing.
    """

    def __init__(
        self: "HttpClient", max_redirects: Optional[int] = MAX_REDIRECTS
    ) -> None:
        self._client = AsyncClient(max_redirects)

    async def __aenter__(self: "HttpClient") -> "HttpClient":
        """Asynchronous context manager entry."""
        return self

    async def __aexit__(
        self: "HttpClient",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Asynchronous context manager exit."""

    async def get(self: "HttpClient", url: str) -> AsyncResponse:
        """
        Send HTTP GET request and receive a response.
        """
        return await self._client.get(url)


__all__ = ["HttpClient", "AsyncResponse"]
