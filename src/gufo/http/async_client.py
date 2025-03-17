# ---------------------------------------------------------------------
# Gufo HTTP: HttpClient implementation
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Asynchronous client."""

# Python modules
from types import TracebackType
from typing import Dict, List, Optional, Type

from . import __version__

# Gufo HTTP modules
from ._fast import (
    BROTLI,
    DEFLATE,
    GZIP,
    AsyncClient,
    AuthBase,
    Proxy,
    RequestMethod,
    Response,
)
from .util import merge_dict

MAX_REDIRECTS = 10
DEFAULT_CONNECT_TIMEOUT = 30.0
DEFAULT_TIMEOUT = 3600.0
NS = 1_000_000_000.0


class HttpClient(object):
    """Asynchronous HTTP client.

    Attributes:
        headers: Headers to be added to every request.
            Used in subclasses.
        user_agent: Default user agent.

    Args:
        max_redirects: Set up redirects policy:

            * **None**: Disable automatic redirect processing.
            * **0**: Deny redirects. Will raise `RedirectError`
                on 3xx response.
            * **>0**: Follow redirects automatically. Will raise
                `RedirectError` when redirects limit exceeded.

        compression: Acceptable compression methods,
            must be a combination of `DEFLATE`, `GZIP`, `BROTLI`, and `ZSTD`.
            Set to `None` to disable compression support.
        validate_cert: Set to `False` to disable TLS certificate
            validation. Otherwise, raise `ConnectionError`
            on invalid certificates.
        connect_timeout: Timeout to establish connection, in seconds.
        timeout: Request timeout, in seconds.
        auth: Authentication settings.
        proxy: Optional list of Proxy istances.
    """

    user_agent = f"Gufo HTTP/{__version__}"
    headers: Optional[Dict[str, bytes]] = None

    def __init__(
        self: "HttpClient",
        /,
        max_redirects: Optional[int] = MAX_REDIRECTS,
        headers: Optional[Dict[str, bytes]] = None,
        compression: Optional[int] = DEFLATE | GZIP | BROTLI,
        validate_cert: bool = True,
        connect_timeout: float = DEFAULT_CONNECT_TIMEOUT,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: Optional[str] = None,
        auth: Optional[AuthBase] = None,
        proxy: Optional[List[Proxy]] = None,
    ) -> None:
        self._client = AsyncClient(
            validate_cert,
            int(connect_timeout * NS),
            int(timeout * NS),
            max_redirects,
            merge_dict(self.headers, headers),
            compression,
            user_agent or self.user_agent,
            auth,
            proxy,
        )

    async def __aenter__(self: "HttpClient") -> "HttpClient":
        """Asynchronous context manager entry.

        Example:
            ``` python
            async with HttpClient() as client:
                ...
            ```
        """
        return self

    async def __aexit__(
        self: "HttpClient",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Asynchronous context manager exit."""

    async def request(
        self: "HttpClient",
        method: RequestMethod,
        url: str,
        /,
        body: Optional[bytes] = None,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        """Send HTTP request and receive a response.

        Args:
            method: Request method
            url: Request url
            body: Request body
            headers: Optional request headers

        Returns:
            Response instance.

        Raises:
            TimeoutError: on timeouts.
            ConnectionError: when failed to establish connection.
            RedirectError: when redirects limit reached.
            RequestError: on other errors related with request processing.
        """
        return await self._client.request(method, url, headers, body)

    async def get(
        self: "HttpClient",
        url: str,
        /,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        """Send HTTP GET request and receive a response.

        Args:
            url: Request url
            headers: Optional request headers

        Returns:
            Response instance.

        Raises:
            TimeoutError: on timeouts.
            ConnectionError: when failed to establish connection.
            RedirectError: when redirects limit reached.
            RequestError: on other errors related with request processing.
        """
        return await self._client.request(RequestMethod.GET, url, headers, None)

    async def head(
        self: "HttpClient",
        url: str,
        /,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        """Send HTTP HEAD request and receive a response.

        Args:
            url: Request url
            headers: Optional request headers

        Returns:
            Response instance.

        Raises:
            TimeoutError: on timeouts.
            ConnectionError: when failed to establish connection.
            RedirectError: when redirects limit reached.
            RequestError: on other errors related with request processing.
        """
        return await self._client.request(RequestMethod.HEAD, url, headers, None)

    async def options(
        self: "HttpClient",
        url: str,
        /,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        """Send HTTP OPTIONS request and receive a response.

        Usually returns `204 No content` response.

        Args:
            url: Request url, use `*` to get options for server.
            headers: Optional request headers.

        Returns:
            Response instance.

        Raises:
            TimeoutError: on timeouts.
            ConnectionError: when failed to establish connection.
            RedirectError: when redirects limit reached.
            RequestError: on other errors related with request processing.
        """
        return await self._client.request(RequestMethod.OPTIONS, url, headers, None)

    async def delete(
        self: "HttpClient",
        url: str,
        /,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        """Send HTTP DELETE request and receive a response.

        Args:
            url: Request url, use `*` to get options for server.
            headers: Optional request headers.

        Returns:
            Response instance.

        Raises:
            TimeoutError: on timeouts.
            ConnectionError: when failed to establish connection.
            RedirectError: when redirects limit reached.
            RequestError: on other errors related with request processing.
        """
        return await self._client.request(RequestMethod.DELETE, url, headers, None)

    async def post(
        self: "HttpClient",
        url: str,
        body: bytes,
        /,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        """Send HTTP POST request and receive a response.

        Args:
            url: Request url, use `*` to get options for server.
            body: Request body.
            headers: Optional request headers.

        Returns:
            Response instance.

        Raises:
            TimeoutError: on timeouts.
            ConnectionError: when failed to establish connection.
            RedirectError: when redirects limit reached.
            RequestError: on other errors related with request processing.
        """
        return await self._client.request(RequestMethod.POST, url, headers, body)

    async def put(
        self: "HttpClient",
        url: str,
        body: bytes,
        /,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        """Send HTTP PUT request and receive a response.

        Args:
            url: Request url, use `*` to get options for server.
            body: Request body.
            headers: Optional request headers.

        Returns:
            Response instance.

        Raises:
            TimeoutError: on timeouts.
            ConnectionError: when failed to establish connection.
            RedirectError: when redirects limit reached.
            RequestError: on other errors related with request processing.
        """
        return await self._client.request(RequestMethod.PUT, url, headers, body)

    async def patch(
        self: "HttpClient",
        url: str,
        body: bytes,
        /,
        headers: Optional[Dict[str, bytes]] = None,
    ) -> Response:
        """Send HTTP PATCH request and receive a response.

        Args:
            url: Request url, use `*` to get options for server.
            body: Request body.
            headers: Optional request headers.

        Returns:
            Response instance.

        Raises:
            TimeoutError: on timeouts.
            ConnectionError: when failed to establish connection.
            RedirectError: when redirects limit reached.
            RequestError: on other errors related with request processing.
        """
        return await self._client.request(RequestMethod.PATCH, url, headers, body)


__all__ = ["HttpClient"]
