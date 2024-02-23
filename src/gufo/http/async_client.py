# ---------------------------------------------------------------------
# Gufo HTTP: HttpClient implementation
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Asynchronous client."""

# Gufo HTTP modules
from ._fast import AsyncClient, AsyncResponse


class HttpClient(object):
    """
    Asynchronous HTTP client.
    """

    def __init__(self: "HttpClient") -> None:
        self._client = AsyncClient()

    async def get(self: "HttpClient", url: str) -> AsyncResponse:
        """
        Send HTTP GET request and receive a response.
        """
        return await self._client.get(url)


__all__ = ["HttpClient", "AsyncResponse"]
