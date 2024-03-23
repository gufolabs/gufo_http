# ---------------------------------------------------------------------
# Gufo HTTP: Tinyproxy context manager
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""Tinyproxy context manager for tests."""

# Python modules
import logging
import queue
import subprocess
import threading
from pathlib import Path
from tempfile import TemporaryDirectory
from types import TracebackType
from typing import Optional, Type

logger = logging.getLogger("gufo.httpd.httpd")


class Tinyproxy(object):
    """
    Tinyproxy test context manager.

    Attributes:
        url: URL for proxy settings.

    Args:
        path: tinyptoxy binary path.
        address: Listen address.
        port: Listen port.
    """

    def __init__(
        self: "Tinyproxy",
        path: str = "/usr/bin/tinyproxy",
        address: str = "127.0.0.1",
        port: int = 10088,
    ) -> None:
        self._path = path
        self._address = address
        self._port = port
        self.url: str = f"http://{address}:{port}"
        self._start_timeout = 5.0
        self._proc = None

    def __enter__(self: "Tinyproxy") -> "Tinyproxy":
        """Context manager entry."""
        self._start()
        return self

    def __exit__(
        self: "Tinyproxy",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Context manager exit."""
        self._stop()

    async def __aenter__(self: "Tinyproxy") -> "Tinyproxy":
        """Asynchronous context manager entry."""
        self._start()
        return self

    async def __aexit__(
        self: "Tinyproxy",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Asynchronous context manager exit."""
        self._stop()

    def get_config(self: "Tinyproxy", prefix: Path) -> str:
        """Generate config."""
        cfg = [
            f"Port {self._port}",
            f"Listen {self._address}",
            "Allow 127.0.0.1",
            "Timeout 600",
            "MaxClients 100",
            "StartServers 5",
        ]
        return "\n".join(cfg)

    def _start(self: "Tinyproxy") -> None:
        logger.info("Starting tinyproxy instance")
        self._dir = TemporaryDirectory(prefix="tp-")
        dn = Path(self._dir.name)
        # Config
        cfg_path = dn / "tinyproxy.conf"
        cfg = self.get_config(cfg_path)
        logger.debug("tinyproxy config:\n%s", cfg)
        with open(cfg_path, "w") as fp:
            fp.write(cfg)
        # Run process
        args = [
            self._path,
            "-d",
            "-c",
            str(cfg_path),
        ]
        self._proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, encoding="utf-8", text=True
        )
        # Wait for nginx is up
        self._wait()
        self._consume_stdout()

    def _wait(self: "Tinyproxy") -> None:
        """Wait until tinyproxy is ready."""
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
            msg = "tinyproxy failed to start"
            logger.error(msg)
            raise TimeoutError(msg)

    def _wait_inner(
        self: "Tinyproxy", q: "queue.Queue[Optional[str]]"
    ) -> None:
        """
        Inner implementation of httpd waiter.

        Launched from the separate thread.

        Args:
            q: Result queue.
        """
        if self._proc and self._proc.stdout:
            logger.info("Waiting for tinyproxy")
            for line in self._proc.stdout:
                logger.debug("tinyproxy: %s", line[:-1])
                if "Accepting connections" in line:
                    logger.info("tinyproxy is up")
                    q.put(None)
                    return
            # Premature termination of snmpd
            logging.error("tinyproxy is terminated prematurely")
            q.put("tinyproxy is terminated prematurely")
            return
        q.put("tinyproxy is not active")

    def _consume_stdout(self: "Tinyproxy") -> None:
        def inner() -> None:
            if self._proc and self._proc.stdout:
                for line in self._proc.stdout:
                    logger.debug("tinyproxy: %s", line[:-1])

        t = threading.Thread(target=inner)
        t.daemon = True
        t.start()

    def _stop(self: "Tinyproxy") -> None:
        """Terminate tinyproxy instance."""
        if self._proc:
            logger.info("Stopping tinyproxy")
            self._proc.kill()
        if self._dir:
            self._dir.cleanup()
