"""Median, IQR and a simple consensus flag for synthetic Delphi ratings."""
from __future__ import annotations

import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def median(values):
    xs = sorted(values)
    n = len(xs)
    if n == 0:
        return 0.0
    mid = n // 2
    if n % 2:
        return float(xs[mid])
    return (xs[mid - 1] + xs[mid]) / 2.0


def quartiles(values):
    xs = sorted(values)
    n = len(xs)
    if n < 2:
        m = float(xs[0]) if xs else 0.0
        return {"q1": m, "median": m, "q3": m, "iqr": 0.0}
    mid = n // 2
    lower = xs[:mid]
    upper = xs[mid:] if n % 2 == 0 else xs[mid + 1:]
    q1 = median(lower)
    q3 = median(upper)
    return {"q1": q1, "median": median(xs), "q3": q3, "iqr": q3 - q1}


def summarise(prop, consensus_iqr=1.5):
    stats = quartiles(prop["ratings"])
    stats["id"] = prop["id"]
    stats["n"] = len(prop["ratings"])
    stats["briefing_hash"] = prop["briefing_hash"]
    stats["consensus"] = stats["iqr"] <= consensus_iqr
    return stats
