#!/usr/bin/env python3
"""Card-debt helpers for Demo 36.

Disclosure debt: cards missing a safety section. Popularity gap: the
most-downloaded cards disclose more often than the long tail.
"""


def missing_safety(cards: list) -> list:
    """Return the sorted ids of cards missing a safety section."""
    return sorted(c["id"] for c in cards if not c.get("safety"))


def popularity_gap(cards: list, top_n: int = 4) -> dict:
    """Split cards by downloads and count missing safety in each tier."""
    ranked = sorted(cards, key=lambda c: c["downloads"], reverse=True)
    top = ranked[:top_n]
    bottom = ranked[top_n:]
    top_missing = sorted(c["id"] for c in top if not c.get("safety"))
    bottom_missing = sorted(c["id"] for c in bottom if not c.get("safety"))
    return {
        "top_ids": [c["id"] for c in top],
        "bottom_ids": [c["id"] for c in bottom],
        "top_missing": top_missing,
        "bottom_missing": bottom_missing,
    }
