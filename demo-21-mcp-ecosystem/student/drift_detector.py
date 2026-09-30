#!/usr/bin/env python3
"""Rug-pull (drift) detector for Demo 21.

A version pair drifts when the description text changes or the permission
set grows. Both signals are exact and deterministic.
"""


def has_drifted(v1: dict | None, v2: dict | None) -> bool:
    """Return True when v2 materially differs from v1."""
    if v1 is None or v2 is None:
        return False
    if v1.get("description") != v2.get("description"):
        return True
    return set(v2.get("permissions", [])) != set(v1.get("permissions", []))
