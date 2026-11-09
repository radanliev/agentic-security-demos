"""Detector transfer from in-distribution stress items to a shifted set."""
from __future__ import annotations

import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def predict(score, threshold):
    return "attack" if score >= threshold else "benign"


def evaluate(cases, threshold):
    tp = fp = tn = fn = 0
    for row in cases:
        pred = predict(row["score"], threshold)
        if row["label"] == "attack" and pred == "attack":
            tp += 1
        elif row["label"] == "benign" and pred == "attack":
            fp += 1
        elif row["label"] == "benign" and pred == "benign":
            tn += 1
        else:
            fn += 1
    n = len(cases)
    attacks = sum(1 for r in cases if r["label"] == "attack")
    return {
        "n": n,
        "recall": round(tp / attacks, 4) if attacks else 0.0,
        "false_positive_rate": round(fp / (fp + tn), 4) if (fp + tn) else 0.0,
        "accuracy": round((tp + tn) / n, 4) if n else 0.0,
        "missed_attacks": fn,
    }


def transfer_gap(in_dist, shifted):
    return {
        "recall_drop": round(in_dist["recall"] - shifted["recall"], 4),
        "accuracy_drop": round(in_dist["accuracy"] - shifted["accuracy"], 4),
    }
