# Python modules
import asyncio

# Third-party modules
import pytest

# Gufo HTTP Modules
from gufo.http.async_client import HttpClient, Response

TEST_URL = "https://docs.gufolabs.com/"


def test_get() -> None:
    async def inner() -> Response:
        client = HttpClient()
        resp = await client.get(TEST_URL)
        assert resp.status == 200
        data = await resp.read()
        assert data

    asyncio.run(inner())


def test_double_read() -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(TEST_URL)
        assert resp.status == 200
        data = await resp.read()
        assert data
        with pytest.raises(RuntimeError):
            await resp.read()

    asyncio.run(inner())
