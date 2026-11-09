"""Equity audit of input guardrails across accessibility-related writing variants.

Defensive and offline. Given scored records from an input guardrail (a score in
[0, 1]; a record is flagged when score >= threshold), each tagged with a writing
variant and a ground-truth label, the functions here report:

* per-variant false-positive and detection rates;
* smoothed disparity ratios against a reference variant;
* paired flip rates for counterfactual pairs (same content, different surface style);
* an audit-only per-variant threshold fit that equalises false-positive rates
  subject to a detection-rate floor.

Variant labels exist only in the audit set. A deployed guardrail must not infer
disability or assistive-technology use; the per-variant fit is an upper bound on
how much of a disparity a threshold change could remove, not a deployable policy.
The records in ``fixtures/`` are synthetic numbers that exercise the code.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Mapping

REFERENCE = "standard"
LABELS = ("benign", "violating")


def _threshold_for(threshold, variant: str) -> float:
    if isinstance(threshold, Mapping):
        return float(threshold[variant])
    return float(threshold)


def flagged(score: float, threshold: float) -> bool:
    return score >= threshold


def rates(records: Iterable[Mapping], threshold) -> dict[str, dict]:
    """Per-variant counts, false-positive rate (fpr) and detection rate (tpr)."""
    counts: dict[str, dict] = defaultdict(lambda: {"benign_n": 0, "fp": 0, "violating_n": 0, "tp": 0})
    for r in records:
        label = r["label"]
        if label not in LABELS:
            raise ValueError(f"unknown label {label!r}")
        row = counts[r["variant"]]
        hit = flagged(r["score"], _threshold_for(threshold, r["variant"]))
        if label == "benign":
            row["benign_n"] += 1
            row["fp"] += int(hit)
        else:
            row["violating_n"] += 1
            row["tp"] += int(hit)
    table = {}
    for variant, row in counts.items():
        row = dict(row)
        row["fpr"] = row["fp"] / row["benign_n"] if row["benign_n"] else None
        row["tpr"] = row["tp"] / row["violating_n"] if row["violating_n"] else None
        table[variant] = row
    return table


def disparity(rate_table: Mapping[str, Mapping], reference: str = REFERENCE, smoothing: float = 0.5) -> dict[str, float]:
    """Ratio of each variant's smoothed false-positive rate to the reference variant's.

    The smoothed rate is (fp + s) / (n + 2s), so that a reference rate of zero does not
    make every ratio infinite; the default s = 0.5 is a Jeffreys-style correction.
    """

    def smoothed(row: Mapping) -> float:
        return (row["fp"] + smoothing) / (row["benign_n"] + 2 * smoothing)

    ref = smoothed(rate_table[reference])
    return {variant: smoothed(row) / ref for variant, row in rate_table.items()}


def paired_flip_rate(records: Iterable[Mapping], threshold, reference: str = REFERENCE) -> dict[str, float | None]:
    """Share of counterfactual pairs whose reference text passes but whose variant text is flagged."""
    pairs: dict[str, dict[str, bool]] = defaultdict(dict)
    for r in records:
        if r["label"] != "benign" or r.get("pair_id") is None:
            continue
        pairs[r["pair_id"]][r["variant"]] = flagged(r["score"], _threshold_for(threshold, r["variant"]))
    tallies: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for pair in pairs.values():
        if reference not in pair or pair[reference]:
            continue
        for variant, hit in pair.items():
            if variant == reference:
                continue
            tallies[variant][1] += 1
            tallies[variant][0] += int(hit)
    return {v: (flips / eligible if eligible else None) for v, (flips, eligible) in tallies.items()}


def fit_thresholds(
    records: Iterable[Mapping], global_threshold: float, target_fpr: float, recall_floor: float
) -> tuple[dict[str, float], list[str]]:
    """Audit-only per-variant thresholds that bring each false-positive rate to the target.

    For each variant the smallest observed score t with FPR(t) <= target_fpr is found and the
    variant threshold becomes max(global_threshold, t), so no variant is screened more strictly
    than under the global policy. If the variant's detection rate at that threshold falls below
    recall_floor, the global threshold is kept and the variant is reported as a conflict for
    human review (fail-closed on detection). Returns (thresholds, conflicts).
    """
    by_variant: dict[str, list[Mapping]] = defaultdict(list)
    for r in records:
        by_variant[r["variant"]].append(r)
    thresholds: dict[str, float] = {}
    conflicts: list[str] = []
    for variant, rows in sorted(by_variant.items()):
        benign = [r["score"] for r in rows if r["label"] == "benign"]
        violating = [r["score"] for r in rows if r["label"] == "violating"]
        candidates = sorted({r["score"] for r in rows}) + [float("inf")]
        chosen = candidates[-1]
        for t in candidates:
            fpr = sum(s >= t for s in benign) / len(benign) if benign else 0.0
            if fpr <= target_fpr:
                chosen = t
                break
        candidate_threshold = max(global_threshold, chosen)
        recall = sum(s >= candidate_threshold for s in violating) / len(violating) if violating else 1.0
        if recall < recall_floor:
            thresholds[variant] = global_threshold
            conflicts.append(variant)
        else:
            thresholds[variant] = candidate_threshold
    return thresholds, conflicts
