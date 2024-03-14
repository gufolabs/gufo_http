# ---------------------------------------------------------------------
# Gufo HTTP: types tests
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Third-party modules
import pytest
from gufo.http import RequestMethod

# Gufo HTTP modules
from gufo.http._fast import DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT


@pytest.mark.parametrize(
    ("method", "expected"),
    [
        (RequestMethod.DELETE, DELETE),
        (RequestMethod.GET, GET),
        (RequestMethod.HEAD, HEAD),
        (RequestMethod.OPTIONS, OPTIONS),
        (RequestMethod.PATCH, PATCH),
        (RequestMethod.POST, POST),
        (RequestMethod.PUT, PUT),
    ],
)
def test_method_code(method: RequestMethod, expected: int) -> None:
    assert method.value == expected


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
def test_method_by_name(name: str, expected: RequestMethod) -> None:
    assert RequestMethod[name] == expected


def test_invalid_method() -> None:
    with pytest.raises(KeyError):
        RequestMethod["foobar"]
