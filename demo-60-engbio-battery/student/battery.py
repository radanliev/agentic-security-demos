"""Score synthetic analysis-task outputs against predeclared references."""
from __future__ import annotations

import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def peak_time(series, times):
    idx = max(range(len(series)), key=lambda i: series[i])
    return times[idx]


def growth_label(series, flat_tol=0.15):
    start, end = series[0], series[-1]
    if abs(end - start) <= flat_tol * start:
        return "flat"
    return "increasing" if end > start else "decreasing"


def construct_ok(sequence, required):
    return all(part in sequence.split("-") for part in required)


def score_task(task):
    kind = task["kind"]
    if kind == "peak":
        pred = peak_time(task["series"], task["times"])
        ok = pred == task["reference"]
    elif kind == "growth":
        pred = growth_label(task["series"])
        ok = pred == task["reference"]
    elif kind == "construct":
        pred = construct_ok(task["sequence"], task["required"])
        ok = pred == task["reference"]
    else:
        raise ValueError("unknown kind")
    return {"id": task["id"], "kind": kind, "predicted": pred, "reference": task["reference"], "correct": ok}


def score_battery(tasks):
    rows = [score_task(t) for t in tasks]
    return {
        "n": len(rows),
        "correct": sum(1 for r in rows if r["correct"]),
        "accuracy": round(sum(1 for r in rows if r["correct"]) / len(rows), 4) if rows else 0.0,
        "rows": rows,
    }
