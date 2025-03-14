# ---------------------------------------------------------------------
# Gufo HTTP: Various utilities
# ---------------------------------------------------------------------
# Copyright (C) 2024, Gufo Labs
# See LICENSE.md for details
# ---------------------------------------------------------------------
"""Various utilities."""

# Python modules
from typing import Dict, Optional


def merge_dict(
    x: Optional[Dict[str, bytes]], y: Optional[Dict[str, bytes]]
) -> Optional[Dict[str, bytes]]:
    """Merge optional dicts of x and y.

    Args:
        x: First dictionary.
        y: Second dictionary.

    Return:
        * None, if both dicts are empty.
        * Resulting merging dict.
    """
    if not x and not y:
        return None
    if x and not y:
        return x
    if not x and y:
        return y
    if x is None or y is None:
        return None  # Shut up mypy
    r: Dict[str, bytes] = {}
    r.update(x)
    r.update(y)
    return r
