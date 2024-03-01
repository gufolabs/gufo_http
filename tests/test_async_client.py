# ---------------------------------------------------------------------
# Gufo HTTP: async HttpClient tests
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import asyncio
from collections.abc import Iterable
from typing import ClassVar, Dict, Optional, Type

# Third-party modules
import pytest
from gufo.http import GZIP

# Gufo HTTP Modules
from gufo.http import (
    RedirectError,
    ConnectError,
    HttpError,
    AlreadyReadError,
    RequestError,
)
from gufo.http.async_client import HttpClient
from gufo.http.httpd import Httpd

from .util import UNROUTABLE_URL, URL_PREFIX, with_env, UNROUTABLE_PROXY


def test_get(httpd: Httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        assert resp.status == 200
        data = await resp.read()
        assert data
        assert b"</html>" in data

    asyncio.run(inner())


def test_head(httpd: Httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.head(f"{URL_PREFIX}/")
        assert resp.status == 200
        data = await resp.read()
        assert data == b""

    asyncio.run(inner())


@pytest.mark.parametrize(
    "url",
    [
        # "*", # Not allowed by reqwest
        f"{URL_PREFIX}/options"
    ],
)
def test_options(httpd: Httpd, url: str) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.options(url)
            assert resp.status == 204
            allow = resp.headers["Allow"]
            for m in (b"OPTIONS", b"GET", b"HEAD"):
                assert m in allow

    asyncio.run(inner())


def test_delete(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.delete(f"{URL_PREFIX}/delete")
            assert resp.status == 200
            data = await resp.read()
            assert data == b"OK"

    asyncio.run(inner())


def test_post(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.post(f"{URL_PREFIX}/post", b"TEST")
            assert resp.status == 200
            data = await resp.read()
            assert data == b"OK"

    asyncio.run(inner())


def test_put(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.put(f"{URL_PREFIX}/put", b"TEST")
            assert resp.status == 200
            data = await resp.read()
            assert data == b"OK"

    asyncio.run(inner())


def test_patch(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.patch(f"{URL_PREFIX}/patch", b"TEST")
            assert resp.status == 200
            data = await resp.read()
            assert data == b"OK"

    asyncio.run(inner())


def test_not_found(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.get(f"{URL_PREFIX}/not_found")
            assert resp.status == 404

    asyncio.run(inner())


def test_double_read(httpd: Httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        assert resp.status == 200
        data = await resp.read()
        assert data
        with pytest.raises(AlreadyReadError):
            await resp.read()

    asyncio.run(inner())


@pytest.mark.parametrize(
    "url", ["ldap://127.0.0.1/", "http://700.700:202020/"]
)
def test_invalid_url(httpd: Httpd, url: str) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            with pytest.raises(RequestError):
                resp = await client.get(url)

    asyncio.run(inner())


def test_no_proxy(httpd: Httpd) -> None:
    async def inner() -> None:
        with with_env({"HTTP_PROXY": UNROUTABLE_PROXY}):
            async with HttpClient() as client:
                resp = await client.get(f"{URL_PREFIX}/")
                assert resp.status == 200
                data = await resp.read()
                assert data
                assert b"</html>" in data

    asyncio.run(inner())


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Content-Type", b"text/html"),
        ("content-type", b"text/html"),
    ],
)
def test_headers_getitem(header: str, expected: bytes, httpd: Httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        h = resp.headers[header]
        assert h == expected

    asyncio.run(inner())


def test_headers_getitem_key_error(httpd: Httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        with pytest.raises(KeyError):
            resp.headers["ctype"]

    asyncio.run(inner())


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("Content-Type", b"text/html"),
        ("content-type", b"text/html"),
        ("ctype", None),
    ],
)
def test_headers_get(
    header: str, expected: Optional[bytes], httpd: Httpd
) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        h = resp.headers.get(header)
        assert h == expected

    asyncio.run(inner())


def test_headers_get_default(httpd: Httpd) -> None:
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
def test_headers_in(header: str, expected: bool, httpd: Httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/")
        r = header in resp.headers
        assert r is expected

    asyncio.run(inner())


def test_headers_keys(httpd: Httpd) -> None:
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


def test_headers_values(httpd: Httpd) -> None:
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


def test_headers_items(httpd: Httpd) -> None:
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


def test_redirect_to_root(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.get(f"{URL_PREFIX}/redirect/root")
            assert resp.status == 200
            data = await resp.read()
            assert data
            assert b"</html>" in data

    asyncio.run(inner())


def test_no_redirect_to_root(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient(max_redirects=None) as client:
            resp = await client.get(f"{URL_PREFIX}/redirect/root")
            assert resp.status == 302

    asyncio.run(inner())


@pytest.mark.parametrize("x", [HttpError, RedirectError])
def test_redirect_to_loop(httpd: Httpd, x: Type[BaseException]) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            with pytest.raises(x):
                await client.get(f"{URL_PREFIX}/redirect/loop")

    asyncio.run(inner())


def test_get_header(httpd: Httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/headers/get")
        assert resp.status == 200
        assert resp.headers["X-Gufo-HTTP"] == b"TEST"
        data = await resp.read()
        assert data
        assert data == b'{"status":true}'

    asyncio.run(inner())


def test_get_without_header(httpd: Httpd) -> None:
    async def inner() -> None:
        client = HttpClient()
        resp = await client.get(f"{URL_PREFIX}/headers/check")
        assert resp.status == 403
        data = await resp.read()
        assert data
        assert data == b'{"status":false}'

    asyncio.run(inner())


class MyHttpClient(HttpClient):
    headers: ClassVar[Dict[str, bytes]] = {"X-Gufo-HTTP": b"TEST"}


def test_get_with_header_class(httpd: Httpd) -> None:
    async def inner() -> None:
        async with MyHttpClient() as client:
            resp = await client.get(f"{URL_PREFIX}/headers/check")
            assert resp.status == 200
            data = await resp.read()
            assert data
            assert data == b'{"status":true}'

    asyncio.run(inner())


def test_get_with_header_client(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient(headers={"X-Gufo-HTTP": b"TEST"}) as client:
            resp = await client.get(f"{URL_PREFIX}/headers/check")
            assert resp.status == 200
            data = await resp.read()
            assert data
            assert data == b'{"status":true}'

    asyncio.run(inner())


def test_get_with_header_request(httpd: Httpd) -> None:
    async def inner() -> None:
        async with HttpClient() as client:
            resp = await client.get(
                f"{URL_PREFIX}/headers/check", headers={"X-Gufo-HTTP": b"TEST"}
            )
            assert resp.status == 200
            data = await resp.read()
            assert data
            assert data == b'{"status":true}'

    asyncio.run(inner())


@pytest.mark.parametrize("compression", [None, GZIP])
def test_compression(compression: Optional[int]) -> None:
    async def inner() -> None:
        async with HttpClient(compression=compression) as client:
            resp = await client.get(f"{URL_PREFIX}/")
            assert resp.status == 200
            data = await resp.read()
            assert data
            assert b"</html>" in data

    asyncio.run(inner())


@pytest.mark.parametrize("x", [HttpError, ConnectError])
def test_connect_timeout(x: Type[BaseException]) -> None:
    async def inner() -> None:
        async with HttpClient(connect_timeout=1.0) as client:
            with pytest.raises(x):
                await client.get(UNROUTABLE_URL)

    asyncio.run(inner())
