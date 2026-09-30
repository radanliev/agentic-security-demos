#!/usr/bin/env python3
"""Coverage helpers for Demo 33.

A gap is an element with a known attack but no stated mitigation.
"""


def gaps(elements: list) -> list:
    """Return the sorted ids of gap elements."""
    return sorted(
        e["id"] for e in elements if e.get("known_attack") and not e.get("stated_mitigation")
    )


def covered(elements: list) -> list:
    """Return the sorted ids of non-gap elements."""
    gap_ids = set(gaps(elements))
    return sorted(e["id"] for e in elements if e["id"] not in gap_ids)
