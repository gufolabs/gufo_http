# Python modules
import asyncio

# Third-party modules
import pytest

# Gufo HTTP Modules
from gufo.http.async_client import HttpClient
from gufo.http import Headers

TEST_URL = "https://docs.gufolabs.com/"


def test_headers() -> None:
    async def get_headers():
        client = HttpClient()
        resp = await client.get(TEST_URL)
        return resp.headers

    # __getitem__
    headers = asyncio.run(get_headers())
    r = headers["Content-Type"]
    assert r == b"text/html; charset=utf-8"
    r = headers["content-type"]
    assert r == b"text/html; charset=utf-8"
    with pytest.raises(KeyError):
        r = headers["gufo-content-type"]
    # get
    r = headers.get("Content-Type")
    assert r == b"text/html; charset=utf-8"
    r = headers.get("content-type")
    assert r == b"text/html; charset=utf-8"
    r = headers.get("gufo-content-type")
    assert r is None
