# ---------------------------------------------------------------------
# Gufo HTTP: Collect PGO data
# ---------------------------------------------------------------------
# Copyright (C) 2024-25, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""Run variuous workload to collect Profile Guided Optimization data."""

# Python modules
import asyncio
import socket

# Gufo HTTP modules
from gufo.http.async_client import HttpClient as AsyncHttpClient
from gufo.http.httpd import Httpd, HttpdMode
from gufo.http.sync_client import HttpClient as SyncHttpClient


def get_free_port() -> int:
    """Get free TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))  # Bind to a random available port
        return sock.getsockname()[1]  # Get assigned port


HTTPD_PATH = "/usr/sbin/nginx"
HTTPD_HOST = "local.gufolabs.com"
HTTPD_ADDRESS = "127.0.0.1"
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
            resp.content.decode()


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
            resp.content.decode()


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
            resp.content.decode()


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
            resp.content.decode()


def main() -> None:
    """Run all tests."""
    # Create HTTP istance
    httpd = Httpd(
        path=HTTPD_PATH,
        address=HTTPD_ADDRESS,
        port=get_free_port(),
        host=HTTPD_HOST,
    )
    httpd._start()
    # Create HTTPS istance
    httpd_ssl = Httpd(
        path=HTTPD_PATH,
        address=HTTPD_ADDRESS,
        port=get_free_port(),
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
