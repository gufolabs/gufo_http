# ---------------------------------------------------------------------
# Gufo HTTP: Httpd context manager
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""Httpd context manager for tests."""

# Python modules
import logging
import os
import queue
import subprocess
import threading
import time
from getpass import getuser
from pathlib import Path
from tempfile import TemporaryDirectory
from types import TracebackType
from typing import Optional, Type

logger = logging.getLogger("gufo.httpd.httpd")


class Httpd(object):
    """
    Httpd test context manager.

    Attributes:
        prefix: URL prefix.

    Args:
        path: nginx binary path.
        address: Listen address.
        port: Listen port.
        host: Server hostname.
        start_timeout: Maximum time to wait for nginx to start.
        check_config: Check nginx config on startup.
    """

    def __init__(
        self: "Httpd",
        path: str = "/usr/sbin/nginx",
        address: str = "127.0.0.1",
        port: int = 10080,
        host: str = "local.gufolabs.com",
        start_timeout: float = 5.0,
        check_config: bool = True,
    ) -> None:
        self._path = path
        self._address = address
        self._port = port
        self._host = host
        self._start_timeout = start_timeout
        self._check_config = True
        self.prefix = f"http://{host}:{port}"

    def __enter__(self: "Httpd") -> "Httpd":
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

    def get_config(self: "Httpd", prefix: Path) -> str:
        """Generate nginx.conf."""
        root = prefix / "data"
        user = getuser()
        user_cfg = f"user {user};" if user == "root" else ""
        pid = root / ".nginx.pid"
        return f"""daemon off;
{user_cfg}
worker_processes auto;
pid {pid};

events {{
    worker_connections 768;
}}

http {{
    sendfile on;
    tcp_nopush on;

    types {{
        text/html                             html htm shtml;
    }}
    default_type application/octet-stream;

    access_log /dev/stdout;
    error_log stderr info;
    gzip on;
    gzip_min_length 5;
    gzip_types text/plain text/css application/json
        application/javascript text/xml application/xml
        application/xml+rss text/javascript;

    server {{
        listen {self._port};
        server_name {self._host};

        location /redirect/root {{
            rewrite ^/redirect/root$ / redirect;
        }}

        location /redirect/loop {{
            rewrite ^/redirect/loop$ /redirect/loop redirect;
        }}

        location /headers/get {{
            add_header X-Gufo-HTTP "TEST";
            return 200 '{{"status":true}}';
        }}

        location /headers/check {{
            if ($http_x_gufo_http != "TEST") {{
                return 403 '{{"status":false}}';
            }}
            return 200 '{{"status":true}}';
        }}

        location /cookie/get {{
            add_header Set-Cookie "gufo-http=test; Path=/";
            return 200 '{{"status":true}}';
        }}

        location /cookie/check {{
            if ($http_cookie !~* "gufo-http=test") {{
                return 403 '{{"status":false}}';
            }}
            return 200 '{{"status":true}}';
        }}

        location /options {{
            if ($request_method = OPTIONS ) {{
                add_header Allow "OPTIONS, GET, HEAD";
                return 204 "No content";
            }}
        }}

        location /delete {{
            limit_except DELETE {{
                deny all;
            }}
            return 200 "OK";
        }}

        location /post {{
            limit_except POST {{
                deny all;
            }}
            return 200 "OK";
        }}

        location /put {{
            limit_except PUT {{
                deny all;
            }}
            return 200 "OK";
        }}

        location /patch {{
            limit_except PATCH {{
                deny all;
            }}
            return 200 "OK";
        }}

        location /ua/default {{
            if ($http_user_agent ~* "^Gufo HTTP/") {{
                return 200 "OK";
            }}
            return 400 "Bad Request";
        }}

        location /ua/custom {{
            if ($http_user_agent ~* "Mozilla") {{
                return 200 "OK";
            }}
            return 400 "Bad Request";
        }}

        location /auth/basic {{
            if ($http_authorization ~* "^Basic (.+)$") {{
                set $basic_token $1;
            }}
            # scott/tiger
            if ($basic_token = "c2NvdHQ6dGlnZXI=") {{
                return 200;
            }}
            return 401;
        }}

        location /auth/bearer {{
            if ($http_authorization ~* "^Bearer (.+)$") {{
                set $bearer_token $1;
            }}

            if ($bearer_token = "123456") {{
                return 200;
            }}
            return 401;
        }}

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
        cfg = self.get_config(dn)
        logger.debug("httpd config:\n%s", cfg)
        cfg_path = dn / "nginx.conf"
        with open(cfg_path, "w") as fp:
            fp.write(cfg)
        # Write data
        os.mkdir(data_path)
        # index.html
        with open(data_path / "index.html", "w") as fp:
            lorem = "lorem ipsum " * 1000
            fp.write(f"<html>{lorem}</html>")
        # bechmarks
        with open(data_path / "bench-1k.txt", "w") as fp:
            fp.write("A" * 1024)
        # Check config
        if self._check_config:
            args = [self._path, "-T", "-c", str(cfg_path)]
            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                text=True,
            )
            o, e = proc.communicate()
            if proc.returncode != 0:
                print(o)
                print(e)
        # Run process
        args = [
            self._path,
            "-q",
            "-g",
            "error_log /dev/null;",
            "-c",
            str(cfg_path),
        ]
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
            time.sleep(1)
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
