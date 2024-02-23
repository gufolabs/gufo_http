# ---------------------------------------------------------------------
# Gufo HTTP: Httpd context manager
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from tempfile import TemporaryDirectory
from types import TracebackType
from typing import List, Optional, Type
from logging import getLogger
from getpass import getuser
from pathlib import Path
import subprocess
import queue
import threading
import logging
import os

logger = logging.getLogger("gufo.httpd.httpd")


class Httpd(object):
    """
    Httpd test context manager.

    Args:
        path: nginx binary path.
        address: Listen address.
        port: Listen port.
        host: Server hostname.
        start_timeout: Maximum time to wait for nginx to start.
    """

    def __init__(
        self: "Httpd",
        path: str = "/usr/sbin/nginx",
        address: str = "127.0.0.1",
        port: int = 10080,
        host: str = "local.gufolabs.com",
        start_timeout: float = 5.0,
    ) -> None:
        self._path = path
        self._address = address
        self._port = port
        self._host = host
        self._start_timeout = start_timeout

    def __enter__(self: "Httpd") -> "Snmpd":
        """Context manager entry."""
        self._start()
        return self

    def __exit__(
        self: "Httpd",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Context manager exit."""
        self._stop()

    async def __aenter__(self: "Httpd") -> "Httpd":
        """Asynchronous context manager entry."""
        self._start()
        return self

    async def __aexit__(
        self: "Httpd",
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Asynchronous context manager exit."""
        self._stop()

    def get_config(self: "Httpd", root: Path) -> str:
        """Generate nginx.conf"""
        user = getuser()
        return f"""daemon off;
user {user};
worker_processes auto;

events {{
    worker_connections 768;
}}

http {{
    sendfile on;
    tcp_nopush on;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /dev/stdout;
    error_log /dev/stdout info;
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    server {{
        listen {self._port};
        server_name {self._host};

        location / {{
            root {root};
        }}
    }}
}}
"""

    def _start(self: "Httpd") -> None:
        logger.info("Starting nginx instance")
        self._dir = TemporaryDirectory(prefix="httpd-")
        dn = Path(self._dir.name)
        data_path = dn / "data"
        cfg = self.get_config(data_path)
        logger.debug("httpd config:\n%s", cfg)
        cfg_path = dn / "nginx.conf"
        with open(cfg_path, "w") as fp:
            fp.write(cfg)
        with open("/tmp/nginx.conf", "w") as fp:
            fp.write(cfg)
        # Write data
        os.mkdir(data_path)
        # index.html
        with open(data_path / "index.html", "w") as fp:
            fp.write("<html>hello</html>")
        # Run process
        args = [self._path, "-c", str(cfg_path)]
        self._proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, encoding="utf-8", text=True
        )
        # Wait for nginx is up
        self._wait()
        self._consume_stdout()

    def _wait(self: "Httpd") -> None:
        """Wait until nginx is ready."""
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
            msg = "nginx failed to start"
            logger.error(msg)
            raise TimeoutError(msg)

    def _wait_inner(self: "Httpd", q: "queue.Queue[Optional[str]]") -> None:
        """
        Inner implementation of httpd waiter.

        Launched from the separate thread.

        Args:
            q: Result queue.
        """
        if self._proc and self._proc.stdout:
            logger.info("Waiting for nginx")
            q.put(None)
            return
            for line in self._proc.stdout:
                logger.debug("nginx: %s", line[:-1])
                if line.startswith("ready"):
                    self.version = line.strip().split(" ", 2)[2].strip()
                    logger.info("nginx is up. Version %s", self.version)
                    q.put(None)
                    return
            # Premature termination of snmpd
            logging.error("nginx is terminated prematurely")
            q.put("nginx is terminated prematurely")
            return
        q.put("nginx is not active")

    def _consume_stdout(self: "Httpd") -> None:
        def inner() -> None:
            if self._proc and self._proc.stdout:
                for line in self._proc.stdout:
                    logger.debug("nginx: %s", line[:-1])

        t = threading.Thread(target=inner)
        t.daemon = True
        t.start()

    def _stop(self: "Httpd") -> None:
        """Terminate nginx instance."""
        if self._proc:
            logger.info("Stopping nginx")
            self._proc.kill()
        if self._dir:
            self._dir.cleanup()