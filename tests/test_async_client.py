# Python modules
import asyncio

# Third-party modules
import pytest

# Gufo HTTP Modules
from gufo.http.async_client import HttpClient, AsyncResponse
from gufo.http.httpd import Httpd
from .util import URL_PREFIX


def test_get(httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        assert resp.status == 200
        data = await resp.read()
        assert data
        assert b"</html>" in data

    asyncio.run(inner())


def test_double_read(httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        assert resp.status == 200
        data = await resp.read()
        assert data
        with pytest.raises(RuntimeError):
            await resp.read()

    asyncio.run(inner())
