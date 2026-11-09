"""Percent agreement and Cohen's kappa on synthetic double-coded documents."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def validate_codebook(data):
    allowed = set(data["codebook"])
    bad = []
    for doc in data["documents"]:
        for key in ("rater_a", "rater_b"):
            if doc[key] not in allowed:
                bad.append((doc["id"], key, doc[key]))
    return bad


def percent_agreement(docs):
    if not docs:
        return 0.0
    agree = sum(1 for d in docs if d["rater_a"] == d["rater_b"])
    return round(agree / len(docs), 4)


def cohen_kappa(docs, codebook):
    n = len(docs)
    if n == 0:
        return 0.0
    po = sum(1 for d in docs if d["rater_a"] == d["rater_b"]) / n
    ca = Counter(d["rater_a"] for d in docs)
    cb = Counter(d["rater_b"] for d in docs)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in codebook)
    if pe == 1:
        return 1.0
    return round((po - pe) / (1 - pe), 4)
