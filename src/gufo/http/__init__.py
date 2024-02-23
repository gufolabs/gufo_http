# ---------------------------------------------------------------------
# Gufo HTTP: Python HTTP Client Library
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

"""Gufo HTTP: The accelerated Python HTTP client library.

Attributes:
    __version__: Current version
"""

# Gufo Labs modules
from ._fast import Headers, HttpError

__version__: str = "0.1.0"
__all__ = ["__version__", "HttpError", "Headers"]
