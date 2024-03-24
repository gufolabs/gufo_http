# ---------------------------------------------------------------------
# Gufo HTTP: ProxyServer context manager
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""ProxyServer context manager for tests."""

# Python modules
import logging
import queue
import subprocess
import threading
from types import TracebackType
from typing import Optional, Type

logger = logging.getLogger("gufo.httpd.httpd")


class ProxyServer(object):
    """
    ProxyServer test context manager.

    Attributes:
        url: URL for proxy settings.

    Args:
        path: tinyptoxy binary path.
        address: Listen address.
        port: Listen port.
    """

    def __init__(
        self: "ProxyServer",
        path: str = "proxy",
        address: str = "127.0.0.1",
        port: int = 10088,
    ) -> None:
        self._path = path
        self._address = address
        self._port = port
        self.url: str = f"http://{address}:{port}"
        self._start_timeout = 5.0
        self._proc = None

    def __enter__(self: "ProxyServer") -> "ProxyServer":
        """Context manager entry."""
        self._start()
        return self

    def __exit__(
        self: "ProxyServer",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Context manager exit."""
        self._stop()

    async def __aenter__(self: "ProxyServer") -> "ProxyServer":
        """Asynchronous context manager entry."""
        self._start()
        return self

    async def __aexit__(
        self: "ProxyServer",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Asynchronous context manager exit."""
        self._stop()

    def _start(self: "ProxyServer") -> None:
        logger.info("Starting proxy.py instance")
        # Run process
        args = [
            self._path,
            f"--host={self._address}",
            f"--port={self._port}",
            "--threadless",
            "--log-level=DEBUG",
            "--log-file=/dev/stdout",
        ]
        self._proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, encoding="utf-8", text=True
        )
        # Wait for nginx is up
        self._wait()
        self._consume_stdout()

    def _wait(self: "ProxyServer") -> None:
        """Wait until proxy.py is ready."""
        if self._proc is None:
            msg = "_wait() must not be started directly"
            raise RuntimeError(msg)
        if not self._proc.stdout:
            msg = "stdout is not piped"
            raise RuntimeError(msg)
        q: queue.Queue[Optional[str]] = queue.Queue()
        t = threading.Thread(target=self._wait_inner, args=[q])
        t.daemon = True
        t.start()
        try:
            err = q.get(block=True, timeout=self._start_timeout)
        except queue.Empty:
            raise TimeoutError from None
        if err is not None:
            raise RuntimeError(err)
        if t.is_alive():
            msg = "proxy.py failed to start"
            logger.error(msg)
            raise TimeoutError(msg)

    def _wait_inner(
        self: "ProxyServer", q: "queue.Queue[Optional[str]]"
    ) -> None:
        """
        Inner implementation of httpd waiter.

        Launched from the separate thread.

        Args:
            q: Result queue.
        """
        if self._proc and self._proc.stdout:
            logger.info("Waiting for proxy.py")
            for line in self._proc.stdout:
                logger.debug("proxy.py: %s", line[:-1])
                if "Started " in line:
                    logger.info("proxy.py is up")
                    q.put(None)
                    return
            # Premature termination of snmpd
            logging.error("proxy.py is terminated prematurely")
            q.put("proxy.py is terminated prematurely")
            return
        q.put("proxy.py is not active")

    def _consume_stdout(self: "ProxyServer") -> None:
        def inner() -> None:
            if self._proc and self._proc.stdout:
                for line in self._proc.stdout:
                    logger.debug("proxy.py: %s", line[:-1])

        t = threading.Thread(target=inner)
        t.daemon = True
        t.start()

    def _stop(self: "ProxyServer") -> None:
        """Terminate proxy.py instance."""
        if self._proc:
            logger.info("Stopping proxy.py")
            self._proc.kill()
