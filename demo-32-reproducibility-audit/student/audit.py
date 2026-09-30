#!/usr/bin/env python3
"""Audit helpers for Demo 32.

Rates: share of papers with code+data, and share that reproduce.
Invariant in the fixture: reproduces implies code+data.
"""


def rates(papers: list) -> dict:
    """Return overall counts and per-channel breakdowns."""
    total = len(papers)
    code_data = sum(1 for p in papers if p.get("code") and p.get("data"))
    reproduces = sum(1 for p in papers if p.get("reproduces"))
    by_channel = {}
    for paper in papers:
        channel = paper.get("channel")
        bucket = by_channel.setdefault(channel, {"n": 0, "reproduces": 0})
        bucket["n"] += 1
        if paper.get("reproduces"):
            bucket["reproduces"] += 1
    return {
        "n": total,
        "code_data": code_data,
        "reproduces": reproduces,
        "by_channel": by_channel,
    }


def invariant_holds(papers: list) -> bool:
    """Return True when every reproducing paper shares code+data."""
    for paper in papers:
        if paper.get("reproduces") and not (paper.get("code") and paper.get("data")):
            return False
    return True
