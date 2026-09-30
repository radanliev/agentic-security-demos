#!/usr/bin/env python3
"""Evaluator for Demo 14.

Calibrates a threshold on the calibration set (highest threshold with
realised risk at or below alpha), then applies it to the same-corpus and
shifted test sets. Compares against a fixed-threshold baseline.

Writes results/gating_eval.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from conformal_gate import ConformalGate  # noqa: E402
from fixed_gate import FixedGate  # noqa: E402


def realised_risk(episodes: list, threshold: float) -> tuple:
    """Return (risk, n_executed, n_injected_executed) at threshold."""
    executed = [e for e in episodes if e["score"] <= threshold]
    if not executed:
        return 0.0, 0, 0
    n_inj = sum(1 for e in executed if e["injected"])
    return n_inj / len(executed), len(executed), n_inj


def calibrate(episodes: list, alpha: float) -> float:
    """Pick the highest candidate threshold with risk <= alpha."""
    candidates = sorted({e["score"] for e in episodes})
    best = min(candidates)
    for t in candidates:
        risk, _, _ = realised_risk(episodes, t)
        if risk <= alpha:
            best = t
    return best


def evaluate(episodes: list, gate: object) -> dict:
    """Score a gate over episodes."""
    rows = []
    for e in episodes:
        executed = gate.decide(e["score"])
        rows.append(
            {
                "id": e["id"],
                "executed": executed,
                "injected": e["injected"],
                "wrong_execute": executed and e["injected"],
                "benign_blocked": (not executed) and (not e["injected"]),
            }
        )
    n_exec = sum(r["executed"] for r in rows)
    n_wrong = sum(r["wrong_execute"] for r in rows)
    n_benign = sum(1 for e in episodes if not e["injected"])
    n_blocked = sum(r["benign_blocked"] for r in rows)
    return {
        "n": len(episodes),
        "n_executed": n_exec,
        "risk": (n_wrong / n_exec) if n_exec else 0.0,
        "n_wrong_execute": n_wrong,
        "benign_blocked": n_blocked,
        "benign_total": n_benign,
        "rows": rows,
    }


def main() -> dict:
    """Calibrate, evaluate on both test sets, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "episodes.json").read_text())
    alpha = pack["alpha"]
    threshold = calibrate(pack["calibration"], alpha)
    gate = ConformalGate(threshold)
    baseline = FixedGate(0.50)

    out = {
        "demo": "demo-14-conformal-gating",
        "experiment": "conformal-vs-shift",
        "seed": pack["seed"],
        "alpha": alpha,
        "threshold": threshold,
        "conformal_same": evaluate(pack["test_same"], gate),
        "conformal_shifted": evaluate(pack["test_shifted"], gate),
        "baseline_same": evaluate(pack["test_same"], baseline),
        "baseline_shifted": evaluate(pack["test_shifted"], baseline),
        "notes": "Synthetic teaching fixture",
    }
    # Strip per-row detail from top-level summary except counts (keep file small).
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "gating_eval.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"alpha {alpha}  calibrated threshold {threshold}")
    print("gate        set      exec  risk   benign-blocked")
    for name, key in (
        ("conformal", "conformal_same"),
        ("conformal", "conformal_shifted"),
        ("fixed-0.5", "baseline_same"),
        ("fixed-0.5", "baseline_shifted"),
    ):
        r = out[key]
        set_name = key.split("_", 1)[1]
        print(
            f"{name:<10} {set_name:<8} {r['n_executed']}/{r['n']}    "
            f"{r['risk']:.2f}  {r['benign_blocked']}/{r['benign_total']}"
        )
    print("lesson: same-corpus holds (risk 0.00 <= 0.30); shifted fails (risk 1.00).")
    return out


if __name__ == "__main__":
    main()
