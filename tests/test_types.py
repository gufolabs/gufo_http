# ---------------------------------------------------------------------
# Gufo HTTP: types tests
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from typing import Optional

# Third-party modules
import pytest

# Gufo HTTP modules
from gufo.http import Proxy, RequestMethod


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("DELETE", RequestMethod.DELETE),
        ("GET", RequestMethod.GET),
        ("HEAD", RequestMethod.HEAD),
        ("OPTIONS", RequestMethod.OPTIONS),
        ("PATCH", RequestMethod.PATCH),
        ("POST", RequestMethod.POST),
        ("PUT", RequestMethod.PUT),
    ],
)
def _test_method_index(name: str, expected: RequestMethod) -> None:
    assert RequestMethod[name] == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("DELETE", RequestMethod.DELETE),
        ("GET", RequestMethod.GET),
        ("HEAD", RequestMethod.HEAD),
        ("OPTIONS", RequestMethod.OPTIONS),
        ("PATCH", RequestMethod.PATCH),
        ("POST", RequestMethod.POST),
        ("PUT", RequestMethod.PUT),
        ("foobar", None),
    ],
)
def test_method_get(name: str, expected: Optional[RequestMethod]) -> None:
    assert RequestMethod.get(name) == expected


def _test_invalid_method() -> None:
    with pytest.raises(KeyError):
        RequestMethod["foobar"]


def test_proxy_invalid_scheme() -> None:
    with pytest.raises(ValueError):
        Proxy("httpz://127.0.0.1:3128/")
