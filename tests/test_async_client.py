# Python modules
import asyncio
from typing import Optional
from collections.abc import Iterable

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


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Content-Type", True),
        ("content-type", True),
        ("ctype", False),
    ],
)
def test_headers_in(header: str, expected: bool, httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        r = header in resp.headers
        assert r is expected

    asyncio.run(inner())


def test_headers_keys(httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        keys = resp.headers.keys()
        assert isinstance(keys, Iterable)
        k = list(keys)
        assert len(k) > 0
        assert "content-type" in k
        assert "server" in k
        assert isinstance(k[0], str)

    asyncio.run(inner())


def test_headers_values(httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        values = resp.headers.values()
        assert isinstance(values, Iterable)
        k = list(values)
        assert len(k) > 0
        assert isinstance(k[0], bytes)
        has_nginx = False
        has_html = False
        for v in k:
            if b"nginx" in v:
                has_nginx = True
            elif b"text/html" in v:
                has_html = True
        assert has_nginx
        assert has_html

    asyncio.run(inner())


def test_headers_items(httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        items = resp.headers.items()
        assert isinstance(items, Iterable)
        k = list(items)
        assert len(k) > 0
        assert isinstance(k[0], tuple)
        assert len(k[0]) == 2
        assert isinstance(k[0][0], str)
        assert isinstance(k[0][1], bytes)
        data = dict(resp.headers.items())
        assert "content-type" in data
        assert b"text/html" in data["content-type"]

    asyncio.run(inner())


def test_redirect_to_root(httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.get(f"{URL_PREFIX}/redirect/root")
            assert resp.status == 200
            data = await resp.read()
            assert data
            assert b"</html>" in data

    asyncio.run(inner())


def test_no_redirect_to_root(httpd) -> None:
    async def inner() -> None:
        async with HttpClient(max_redirects=None) as client:
            resp = await client.get(f"{URL_PREFIX}/redirect/root")
            assert resp.status == 302

    asyncio.run(inner())


def test_redirect_to_loop(httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            with pytest.raises(RuntimeError):
                resp = await client.get(f"{URL_PREFIX}/redirect/loop")

    asyncio.run(inner())


def test_get_header(httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/headers/get")
        assert resp.status == 200
        assert resp.headers["X-Gufo-HTTP"] == b"TEST"
        data = await resp.read()
        assert data
        assert data == b'{"status":true}'

    asyncio.run(inner())
