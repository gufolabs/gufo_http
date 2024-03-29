# ---------------------------------------------------------------------
# Gufo HTTP: Collect PGO data
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""Run variuous workload to collect Profile Guided Optimization data"""

# Python modules
import asyncio
import random

# Gufo HTTP modules
from gufo.http.httpd import Httpd, HttpdMode
from gufo.http.sync_client import HttpClient as SyncHttpClient
from gufo.http.async_client import HttpClient as AsyncHttpClient


HTTPD_PATH = "/usr/sbin/nginx"
HTTPD_HOST = "local.gufolabs.com"
HTTPD_ADDRESS = "127.0.0.1"
HTTPD_PORT = random.randint(52000, 53999)
HTTPD_SSL_PORT = random.randint(52000, 53999)
REPEATS = 100


def run_single_sync(prefix: str) -> None:
    """
    Single requests with sync client.

    Args:
        prefix: URL prefix
    """
    url = f"{prefix}/bench-1k.txt"
    for _ in range(REPEATS):
        with SyncHttpClient(validate_cert=False) as client:
            resp = client.get(url)
            resp.read()


async def run_single_async(prefix: str) -> None:
    """
    Single requests with async client.

    Args:
        prefix: URL prefix
    """
    url = f"{prefix}/bench-1k.txt"
    for _ in range(REPEATS):
        async with AsyncHttpClient(validate_cert=False) as client:
            resp = await client.get(url)
            await resp.read()


def run_linear_sync(prefix: str) -> None:
    """
    Linear requests with sync client.

    Args:
        prefix: URL prefix
    """
    url = f"{prefix}/bench-1k.txt"
    with SyncHttpClient(validate_cert=False) as client:
        for _ in range(REPEATS):
            resp = client.get(url)
            resp.read()


async def run_linear_async(prefix: str) -> None:
    """
    Linear requests with async client.

    Args:
        prefix: URL prefix
    """
    url = f"{prefix}/bench-1k.txt"
    async with AsyncHttpClient(validate_cert=False) as client:
        for _ in range(REPEATS):
            resp = await client.get(url)
            await resp.read()


def main() -> None:
    """Run all tests."""
    # Create HTTP istance
    httpd = Httpd(
        path=HTTPD_PATH,
        address=HTTPD_ADDRESS,
        port=HTTPD_PORT,
        host=HTTPD_HOST,
    )
    httpd._start()
    # Create HTTPS istance
    httpd_ssl = Httpd(
        path=HTTPD_PATH,
        address=HTTPD_ADDRESS,
        port=HTTPD_SSL_PORT,
        host=HTTPD_HOST,
        mode=HttpdMode.HTTPS,
    )
    httpd_ssl._start()
    # Run tests
    # HTTP
    run_single_sync(httpd.prefix)
    asyncio.run(run_single_async(httpd.prefix))
    run_linear_sync(httpd.prefix)
    asyncio.run(run_linear_async(httpd.prefix))
    # SSL
    run_single_sync(httpd_ssl.prefix)
    asyncio.run(run_single_async(httpd_ssl.prefix))
    run_linear_sync(httpd_ssl.prefix)
    asyncio.run(run_linear_async(httpd_ssl.prefix))


if __name__ == "__main__":
    main()
