"""Normal-approximation power for a two-sample mean difference (equal n, equal sd)."""
from __future__ import annotations

import json
import math
from pathlib import Path

# Two-sided z critical values used by the teaching demo (no SciPy).
Z_CRIT = {0.05: 1.95996398454, 0.01: 2.57582930355}


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def se_diff(sd, n_per_arm):
    return sd * math.sqrt(2.0 / n_per_arm)


def power_two_sample(delta, sd, n_per_arm, alpha=0.05):
    if alpha not in Z_CRIT:
        raise ValueError("this teaching helper only tabulates alpha 0.05 and 0.01")
    zc = Z_CRIT[alpha]
    se = se_diff(sd, n_per_arm)
    # 1 - Phi(zc - |delta|/se) + Phi(-zc - |delta|/se); the second term is tiny here.
    z = abs(delta) / se
    # Abramowitz-Stegun-style erf for Phi
    def phi(x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    return round(1.0 - phi(zc - z) + phi(-zc - z), 4)


def plan_table(cfg):
    return {
        "n_per_arm": cfg["n_per_arm"],
        "alpha": cfg["alpha"],
        "sd": cfg["sd"],
        "immediate_power": power_two_sample(cfg["raw_difference"], cfg["sd"], cfg["n_per_arm"], cfg["alpha"]),
        "residual_power": power_two_sample(cfg["residual_difference"], cfg["sd"], cfg["n_per_arm"], cfg["alpha"]),
    }
