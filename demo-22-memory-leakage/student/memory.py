#!/usr/bin/env python3
"""Memory-leakage checks for Demo 22.

Three tiny predicates over synthetic memory entries:

- persists_high: high-sensitivity entries that were persisted (violations).
- resurfaced: entries that reappeared in another session/user.
- erasure_failures: entries marked deleted but still present (persisted).
"""


def persists_high(entries: list) -> list:
    """Return ids of high-sensitivity entries that were persisted."""
    return [
        e["id"]
        for e in entries
        if e.get("sensitivity") == "high" and e.get("persisted")
    ]


def resurfaced(entries: list) -> list:
    """Return ids of entries that resurfaced in another session/user."""
    return [e["id"] for e in entries if e.get("resurfaced_in")]


def erasure_failures(entries: list) -> list:
    """Return ids of entries marked deleted but still present."""
    return [
        e["id"] for e in entries if e.get("deleted") and e.get("persisted")
    ]
