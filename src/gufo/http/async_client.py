# ---------------------------------------------------------------------
# Gufo HTTP: HttpClient implementation
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
from ._fast import AsyncClient, AsyncResponse


class HttpClient(object):
    def __init__(self: "HttpClient") -> None:
        self._client = AsyncClient()

    async def get(self: "HttpClient", url: str) -> AsyncResponse:
        return await self._client.get(url)
