# ---------------------------------------------------------------------
# Gufo HTTP: Benchmarks
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import asyncio
import io
import random
import urllib.request
from typing import Iterable

# Third-party modules
import aiohttp
import aiosonic
import httpx
import niquests
import pycurl
import pytest
import requests
import urllib3

# Gufo HTTP modules
from gufo.http.async_client import HttpClient as AsyncHttpClient
from gufo.http.httpd import Httpd
from gufo.http.sync_client import HttpClient as SyncHttpClient

HTTPD_PATH = "/usr/sbin/nginx"
HTTPD_HOST = "local.gufolabs.com"
HTTPD_ADDRESS = "127.0.0.1"
HTTPD_PORT = random.randint(52000, 53999)


@pytest.fixture(scope="session")
def httpd() -> Iterable[Httpd]:
    with Httpd(
        path=HTTPD_PATH,
        address=HTTPD_ADDRESS,
        port=HTTPD_PORT,
        host=HTTPD_HOST,
    ) as httpd:
        yield httpd


def test_gufo_http_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        with SyncHttpClient() as client:
            resp = client.get(url)
            _ = resp.content


def test_gufo_http_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        async def inner():
            async with AsyncHttpClient() as client:
                resp = await client.get(url)
                _ = resp.content

        asyncio.run(inner())


def test_requests_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        resp = requests.get(url)
        _ = resp.content


def test_niquests_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        session = niquests.Session(multiplexed=True)
        resp = session.get(url)
        _ = resp.content


def test_httpx_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        with httpx.Client() as client:
            resp = client.get(url)
            _ = resp.text


def test_httpx_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        async def inner():
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                _ = resp.text

        asyncio.run(inner())


def test_aiohttp_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        async def inner():
            async with aiohttp.ClientSession() as client:
                resp = await client.get(url)
                await resp.read()

        asyncio.run(inner())


def test_aiosonic_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        async def inner():
            client = aiosonic.HTTPClient()
            resp = await client.get(url)
            await resp.content()

        asyncio.run(inner())


def test_urllib_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        with urllib.request.urlopen(url) as resp:
            resp.read()


def test_urllib3_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        resp = urllib3.request("GET", url)
        _ = resp.data


def test_pycurl_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        curl = pycurl.Curl()
        buffer = io.BytesIO()
        curl.setopt(curl.URL, url)
        curl.setopt(curl.WRITEDATA, buffer)
        curl.perform()
        _body = buffer.getvalue()
        curl.close()
