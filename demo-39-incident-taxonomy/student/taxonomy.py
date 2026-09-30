#!/usr/bin/env python3
"""Practitioner taxonomy helpers for Demo 39.

Tallies attack patterns over ten synthetic incident sketches and counts
supported entries in the static control catalogue. The tallies are
properties of the hand-built fixture, not field measurements.
"""


def top_pattern(incidents: list) -> dict:
    """Return the most frequent pattern and its count."""
    counts: dict = {}
    for inc in incidents:
        counts[inc["pattern"]] = counts.get(inc["pattern"], 0) + 1
    best = max(sorted(counts), key=lambda p: counts[p])
    return {"pattern": best, "count": counts[best], "n": len(incidents),
            "counts": counts}


def supported_controls(controls: list) -> dict:
    """Count supported entries in the static control catalogue."""
    supported = [c["id"] for c in controls if c["supported"]]
    return {"n": len(controls), "supported": len(supported),
            "supported_ids": supported}
