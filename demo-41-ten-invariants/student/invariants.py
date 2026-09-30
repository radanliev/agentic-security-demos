#!/usr/bin/env python3
"""Ten-invariant checklist evaluator for Demo 41.

Splits ten synthetic invariant checks into holding and violated sets.
Verdicts are hand-picked properties of the fixture, not evidence about
real systems: no invariant here is backed by anything but the toy file.
"""


def evaluate(checks: list) -> dict:
    """Return holding/violated partition with counts."""
    holding = [c["name"] for c in checks if c["holds"]]
    violated = [c["name"] for c in checks if not c["holds"]]
    return {"n": len(checks), "holding": holding, "violated": violated,
            "n_holding": len(holding), "n_violated": len(violated)}
