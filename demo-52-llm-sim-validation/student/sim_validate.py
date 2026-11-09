"""Held-out validation and a contamination probe for toy cohort simulators."""
from __future__ import annotations

import json
from pathlib import Path


def load_cohorts(path: Path) -> dict:
    return json.loads(path.read_text())


def mae(pairs):
    if not pairs:
        return 0.0
    return sum(abs(a - b) for a, b in pairs) / len(pairs)


def honest_predict(train, target):
    """Use the same module if seen, honouring a rename alias, otherwise the train mean."""
    name = target.get("alias_of", target["module"])
    matches = [r for r in train if r["module"] == name]
    if matches:
        src = matches[0]
        return {"pass_rate": src["pass_rate"], "withdraw_rate": src["withdraw_rate"], "source": "same-module"}
    n = len(train)
    return {
        "pass_rate": sum(r["pass_rate"] for r in train) / n,
        "withdraw_rate": sum(r["withdraw_rate"] for r in train) / n,
        "source": "train-mean",
    }


def memorizer_predict(train, target):
    """Recite a published row by name. Fails the rename probe."""
    for r in train:
        if r["module"] == target["module"]:
            return {"pass_rate": r["pass_rate"], "withdraw_rate": r["withdraw_rate"], "source": "memorized-name"}
    return {"pass_rate": 0.0, "withdraw_rate": 0.0, "source": "unknown-name"}


def score_heldout(predict, train, heldout):
    pairs_pass, pairs_wd = [], []
    for row in heldout:
        pred = predict(train, row)
        pairs_pass.append((pred["pass_rate"], row["pass_rate"]))
        pairs_wd.append((pred["withdraw_rate"], row["withdraw_rate"]))
    return {"pass_mae": round(mae(pairs_pass), 4), "withdraw_mae": round(mae(pairs_wd), 4)}


def contamination_probe(predict, train, probe):
    honest_on_true = honest_predict(train, {"module": probe["true_module"], "year": probe["year"]})
    presented = {"module": probe["presented_as"], "year": probe["year"], "alias_of": probe["true_module"]}
    # Honest predictors receive the alias; memorizers ignore it and key on presented_as.
    pred = predict(train, presented)
    failed = pred["source"] in {"memorized-name", "unknown-name"} and pred["pass_rate"] != honest_on_true["pass_rate"]
    return {
        "presented_as": probe["presented_as"],
        "true_module": probe["true_module"],
        "predicted_pass": pred["pass_rate"],
        "expected_if_transfer": honest_on_true["pass_rate"],
        "failed_to_transfer": failed,
        "source": pred["source"],
    }
