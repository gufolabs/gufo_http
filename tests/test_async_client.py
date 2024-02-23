# Python modules
import asyncio
from typing import Optional

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


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Content-Type", b"text/html"),
        ("content-type", b"text/html"),
    ],
)
def test_headers_getitem(header: str, expected: bytes, httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        h = resp.headers[header]
        assert h == expected

    asyncio.run(inner())


def test_headers_getitem_key_error(httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        with pytest.raises(KeyError):
            h = resp.headers["ctype"]

    asyncio.run(inner())


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Content-Type", b"text/html"),
        ("content-type", b"text/html"),
        ("ctype", None),
    ],
)
def test_headers_get(header: str, expected: Optional[bytes], httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        h = resp.headers.get(header)
        assert h == expected

    asyncio.run(inner())


def test_headers_get_default(httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        default = b"default/value"
        h = resp.headers.get("ctype", default)
        assert h == default
        # assert h is default

    asyncio.run(inner())
