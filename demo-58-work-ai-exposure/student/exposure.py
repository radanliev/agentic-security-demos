"""Task-level exposure summaries on synthetic occupation rows."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def occupation_mean(occ):
    tasks = occ["tasks"]
    return round(sum(t["exposure"] for t in tasks) / len(tasks), 4)


def family_means(occupations):
    buckets = defaultdict(list)
    for occ in occupations:
        buckets[occ["family"]].append(occupation_mean(occ))
    return {fam: round(sum(vs) / len(vs), 4) for fam, vs in sorted(buckets.items())}


def agentic_share(occupations):
    tasks = [t for occ in occupations for t in occ["tasks"]]
    return round(sum(1 for t in tasks if t["agentic"]) / len(tasks), 4)
