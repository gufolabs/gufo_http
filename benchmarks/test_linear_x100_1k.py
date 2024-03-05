# ---------------------------------------------------------------------
# Gufo HTTP: Benchmarks
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import asyncio
import random
import urllib.request
from typing import Iterable

# Third-party modules
import aiohttp
import httpx
import pytest
import requests

# Gufo HTTP modules
from gufo.http.async_client import HttpClient as AsyncHttpClient
from gufo.http.httpd import Httpd
from gufo.http.sync_client import HttpClient as SyncHttpClient

HTTPD_PATH = "/usr/sbin/nginx"
HTTPD_HOST = "local.gufolabs.com"
HTTPD_ADDRESS = "127.0.0.1"
HTTPD_PORT = random.randint(52000, 53999)
REPEATS = 100


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
            for _ in range(REPEATS):
                resp = client.get(url)
                resp.read()


def test_gufo_http_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        async def inner():
            async with AsyncHttpClient() as client:
                for _ in range(REPEATS):
                    resp = await client.get(url)
                    await resp.read()

        asyncio.run(inner())


def test_requests_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        for _ in range(REPEATS):
            resp = requests.get(url)
            _ = resp.content


def test_httpx_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        with httpx.Client() as client:
            for _ in range(REPEATS):
                resp = client.get(url)
                _ = resp.text


def test_httpx_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        async def inner():
            async with httpx.AsyncClient() as client:
                for _ in range(REPEATS):
                    resp = await client.get(url)
                    _ = resp.text

        asyncio.run(inner())


def test_aiohttp_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        async def inner():
            async with aiohttp.ClientSession() as client:
                for _ in range(REPEATS):
                    resp = await client.get(url)
                    await resp.read()

        asyncio.run(inner())


def test_urllib_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    @benchmark
    def bench():
        for _ in range(REPEATS):
            with urllib.request.urlopen(url) as resp:
                resp.read()
