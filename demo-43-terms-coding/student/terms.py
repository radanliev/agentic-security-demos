#!/usr/bin/env python3
"""Platform-terms coding helpers for Demo 43.

Tallies three accountability clauses over eight synthetic platform-terms
codings. The tallies are properties of the hand-built fixture, not
measurements of real terms of service.
"""

CLAUSES = ("disclaims_autonomy", "requires_monitoring", "consent_for_delegation")


def tally(platforms: list) -> dict:
    """Count True for each accountability clause."""
    counts = {clause: sum(1 for p in platforms if p.get(clause, False))
              for clause in CLAUSES}
    return {"n": len(platforms), "counts": counts}
