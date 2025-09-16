# ---------------------------------------------------------------------
# Gufo HTTP: Test utilities
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
import contextlib
import os
import shutil
from typing import Dict


def _get_nginx_path() -> str:
    """Detect nginx' path."""
    # Default place
    path = "/usr/sbin/nginx"
    # Darwin and others
    if not os.path.exists(path):
        path = shutil.which("nginx") or ""
    return path


HTTPD_PATH = _get_nginx_path()
HTTPD_HOST = "local.gufolabs.com"
HTTPD_ADDRESS = "127.0.0.1"
UNROUTABLE_URL = "http://192.0.2.1/"
UNROUTABLE_PROXY = "http://192.0.2.1:3128/"
TEXT_PLAIN = "text/plain"


@contextlib.contextmanager
def with_env(env: Dict[str, str]) -> None:
    """Temporary setup environment variables.

    Set up environment variables during context
    and restore previous state on exit.
    """
    # Store state
    _prev = {k: os.environ.get(k) for k in env}
    # Setup
    for k, v in env.items():
        os.environ[k] = v
    # Return control into context
    yield
    # Restore
    for k, v in _prev.items():
        if v is None and k in os.environ:
            del os.environ[k]
        elif v is not None:
            os.environ[k] = v
