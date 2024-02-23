# ---------------------------------------------------------------------
# Gufo Ping: HTTP Client Library
# Python build
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# ---------------------------------------------------------------------

# Python modules
from typing import Optional, Sequence
import os

# Third-party modules
from setuptools import setup
from setuptools_rust import RustExtension


def _from_env(name: str) -> Optional[Sequence[str]]:
    v = os.environ.get(name, "").strip()
    if not v:
        return None
    return v.split()


def get_rustc_flags() -> Optional[Sequence[str]]:
    return _from_env("BUILD_RUSTC_FLAGS")


def get_cargo_flags() -> Optional[Sequence[str]]:
    return _from_env("BUILD_CARGO_FLAGS")


setup(
    rust_extensions=[
        RustExtension(
            "gufo.http._fast",
            args=get_cargo_flags(),
            rustc_flags=get_rustc_flags(),
        )
    ],
)
