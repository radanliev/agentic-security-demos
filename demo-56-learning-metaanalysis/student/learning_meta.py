"""Inverse-variance fixed-effect mean and Cochran Q on synthetic studies."""
from __future__ import annotations

import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def fixed_effect(studies):
    weights = [1.0 / s["vi"] for s in studies]
    wsum = sum(weights)
    mean = sum(w * s["yi"] for w, s in zip(weights, studies)) / wsum
    q = sum(w * (s["yi"] - mean) ** 2 for w, s in zip(weights, studies))
    return {
        "k": len(studies),
        "mean": round(mean, 4),
        "se": round((1.0 / wsum) ** 0.5, 4),
        "Q": round(q, 4),
        "df": len(studies) - 1,
    }
