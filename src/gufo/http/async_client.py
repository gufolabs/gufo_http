# ---------------------------------------------------------------------
# Gufo HTTP: HttpClient implementation
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Asynchronous client."""

# Python modules
from types import TracebackType
from typing import Dict, Optional, Type

# Gufo HTTP modules
from ._fast import AsyncClient, AsyncResponse
from .util import merge_dict

MAX_REDIRECTS = 10


class HttpClient(object):
    """
    Asynchronous HTTP client.

    Attributes:
        headers: Headers to be added to every request.
            Used in subclasses.

    Args:
        max_redirects: Maximal amount of redirects. Use `None`
            to disable redirect processing.
    """

    headers: Optional[Dict[str, bytes]] = None

    def __init__(
        self: "HttpClient",
        max_redirects: Optional[int] = MAX_REDIRECTS,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> None:
        self._client = AsyncClient(
            max_redirects, merge_dict(self.headers, headers)
        )

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

    async def get(
        self: "HttpClient",
        url: str,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> AsyncResponse:
        """
        Send HTTP GET request and receive a response.

        Args:
            url: Request url
            headers: Optional request headers

        Returns:
            AsyncResponse instance.
        """
        return await self._client.get(url, headers)


__all__ = ["HttpClient", "AsyncResponse"]
