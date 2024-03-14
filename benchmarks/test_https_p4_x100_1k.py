# ---------------------------------------------------------------------
# Gufo HTTP: Benchmarks
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import asyncio
import concurrent.futures
import io
import random
import ssl
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
from gufo.http.httpd import Httpd, HttpdMode
from gufo.http.sync_client import HttpClient as SyncHttpClient

HTTPD_PATH = "/usr/sbin/nginx"
HTTPD_HOST = "local.gufolabs.com"
HTTPD_ADDRESS = "127.0.0.1"
HTTPD_PORT = random.randint(52000, 53999)
REPEATS = 100
CONCURRENCY = 4  # Must divide repeats
PER_TASK = REPEATS // CONCURRENCY


@pytest.fixture(scope="session")
def httpd() -> Iterable[Httpd]:
    with Httpd(
        path=HTTPD_PATH,
        address=HTTPD_ADDRESS,
        port=HTTPD_PORT,
        host=HTTPD_HOST,
        mode=HttpdMode.HTTPS,
    ) as httpd:
        yield httpd


def run_on_threadpool(fn):
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=CONCURRENCY
    ) as executor:
        futures = [executor.submit(fn) for _ in range(CONCURRENCY)]
        concurrent.futures.wait(futures)


async def run_async(fn):
    tasks = [asyncio.create_task(fn()) for _ in range(CONCURRENCY)]
    await asyncio.gather(*tasks)


def test_gufo_http_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    def do_request():
        with SyncHttpClient(validate_cert=False) as client:
            for _ in range(PER_TASK):
                resp = client.get(url)
                _ = resp.content

    @benchmark
    def bench():
        run_on_threadpool(do_request)


def test_gufo_http_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    async def do_request():
        async with AsyncHttpClient(validate_cert=False) as client:
            for _ in range(PER_TASK):
                resp = await client.get(url)
                _ = resp.content

    @benchmark
    def bench():
        asyncio.run(run_async(do_request))


def test_requests_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    def do_request():
        for _ in range(PER_TASK):
            resp = requests.get(url, verify=False)
            _ = resp.content

    @benchmark
    def bench():
        run_on_threadpool(do_request)


def test_niquests_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    def do_request():
        session = niquests.Session(multiplexed=True)
        for _ in range(PER_TASK):
            resp = session.get(url, verify=False)
            _ = resp.content

    @benchmark
    def bench():
        run_on_threadpool(do_request)


def test_httpx_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    def do_request():
        with httpx.Client(verify=False) as client:
            for _ in range(PER_TASK):
                resp = client.get(url)
                _ = resp.text

    @benchmark
    def bench():
        run_on_threadpool(do_request)


def test_httpx_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    async def do_request():
        async with httpx.AsyncClient(verify=False) as client:
            for _ in range(PER_TASK):
                resp = await client.get(url)
                _ = resp.text

    @benchmark
    def bench():
        asyncio.run(run_async(do_request))


def test_aiohttp_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    async def do_request():
        async with aiohttp.ClientSession() as client:
            for _ in range(PER_TASK):
                resp = await client.get(url, verify_ssl=False)
                await resp.read()

    @benchmark
    def bench():
        asyncio.run(run_async(do_request))


def test_aiosonic_async(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    async def do_request():
        client = aiosonic.HTTPClient(verify_ssl=False)
        for _ in range(PER_TASK):
            resp = await client.get(url)
            await resp.content()

    @benchmark
    def bench():
        asyncio.run(run_async(do_request))


def test_urllib_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"
    # Disable TLS certificate validation
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    def do_request():
        for _ in range(PER_TASK):
            with urllib.request.urlopen(url, context=context) as resp:
                resp.read()

    @benchmark
    def bench():
        run_on_threadpool(do_request)


def test_urllib3_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    def do_request():
        pool = urllib3.HTTPSConnectionPool(
            httpd._host,
            port=httpd._port,
            cert_reqs="CERT_NONE",
            assert_hostname=False,
        )
        for _ in range(PER_TASK):
            resp = pool.request("GET", url)
            _ = resp.data

    @benchmark
    def bench():
        run_on_threadpool(do_request)


def test_pycurl_sync(httpd: Httpd, benchmark) -> None:
    url = f"{httpd.prefix}/bench-1k.txt"

    def do_request():
        curl = pycurl.Curl()
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        for _ in range(PER_TASK):
            buffer = io.BytesIO()
            curl.setopt(curl.URL, url)
            curl.setopt(curl.WRITEDATA, buffer)
            curl.perform()
            _body = buffer.getvalue()
        curl.close()

    @benchmark
    def bench():
        run_on_threadpool(do_request)
