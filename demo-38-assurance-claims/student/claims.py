#!/usr/bin/env python3
"""Coverage coding for Demo 38.

Counts, over eight synthetic system-card codings, how many cards cover each
assurance obligation and how many cover all of them. The counts are
properties of the hand-built fixture, not measurements of real cards.
"""


def coverage(cards: list, obligations: list) -> dict:
    """Return per-obligation counts, full-coverage count, and weakest link."""
    per_obligation = {
        ob: sum(1 for c in cards if c.get(ob, False)) for ob in obligations
    }
    full = sum(1 for c in cards if all(c.get(ob, False) for ob in obligations))
    weakest = min(obligations, key=lambda ob: (per_obligation[ob], ob))
    return {
        "n": len(cards),
        "per_obligation": per_obligation,
        "full_coverage": full,
        "weakest": weakest,
        "weakest_count": per_obligation[weakest],
    }
