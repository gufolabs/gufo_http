# ---------------------------------------------------------------------
# Gufo HTTP: Utilities tests
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------

# Python modules
from typing import Dict, Optional

# Third-party modules
import pytest

# Gufo HTTP modules
from gufo.http.util import merge_dict


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (None, None, None),
        ({"x": b"1", "y": b"2"}, None, {"x": b"1", "y": b"2"}),
        (None, {"x": b"1", "y": b"2"}, {"x": b"1", "y": b"2"}),
        (
            {"x": b"1", "y": b"2"},
            {"x": b"3", "z": b"4"},
            {"x": b"3", "y": b"2", "z": b"4"},
        ),
    ],
)
def test_merge_dict(
    x: Optional[Dict[str, bytes]],
    y: Optional[Dict[str, bytes]],
    expected: Optional[Dict[str, bytes]],
) -> None:
    r = merge_dict(x, y)
    assert r == expected
