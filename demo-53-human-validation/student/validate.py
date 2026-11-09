"""Sampled validation of agent outputs with planted errors."""
from __future__ import annotations

import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def planted(items):
    return [i for i in items if i["planted_error"]]


def sample(items, sample_ids):
    wanted = set(sample_ids)
    return [i for i in items if i["id"] in wanted]


def coverage(items, sample_ids):
    """Share of planted errors that landed in the audited sample."""
    plants = planted(items)
    sampled = {i["id"] for i in sample(items, sample_ids)}
    found = [p for p in plants if p["id"] in sampled]
    return {
        "planted": len(plants),
        "planted_in_sample": len(found),
        "coverage": round(len(found) / len(plants), 4) if plants else 0.0,
    }


def design_based_error_rate(items, sample_ids):
    """If every sampled planted error is caught, estimate the population error rate from the sample."""
    sampled = sample(items, sample_ids)
    if not sampled:
        return 0.0
    return round(sum(1 for i in sampled if i["planted_error"]) / len(sampled), 4)
