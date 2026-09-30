#!/usr/bin/env python3
"""Patch-lifecycle helpers for Demo 42.

Computes the median fix-to-adoption lag and counts fixes blocked by
version pins over eight synthetic vulnerability records. The figures are
hand-picked properties of the fixture, not ecosystem measurements.
"""


def median(values: list) -> float:
    """Return the median of a non-empty list of numbers."""
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def blocked(vulns: list) -> list:
    """Return the ids of vulns whose adoption is blocked by a pin."""
    return [v["id"] for v in vulns if v["blocked_by_pin"]]
