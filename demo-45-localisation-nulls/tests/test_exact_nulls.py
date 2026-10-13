import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))

from nulls import lift, required_pool, scores, tail  # noqa: E402


def test_known_tail():
    assert tail(45, 10, 8, 5) == pytest.approx(0.0082510259, rel=1e-6)


def test_scores_rank_with_tp():
    prev = None
    for tp in range(0, 9):
        r, p, f = scores(10, 8, tp)
        cur = (r, p, f)
        if prev is not None:
            assert cur > prev
        prev = cur


def test_transfer_pair_same_recall_different_p():
    a = tail(60, 12, 6, 6)
    b = tail(30, 12, 6, 6)
    assert a < b
    assert b / a > 50  # geometry moves the null ~84x here
    assert lift(60, 12, 6, 6) != pytest.approx(lift(30, 12, 6, 6))


def test_design_limit():
    assert required_pool(10, 2, 0.01) == 96
    assert required_pool(10, 2, 0.05) == 43
    assert tail(20, 4, 2, 2) > 0.01  # max TP at k=2 cannot clear alpha here


def test_run_writes_results_parity():
    r = subprocess.run(
        [sys.executable, "student/run_nulls.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads((ROOT / "results" / "nulls.json").read_text())
    assert len(data["rows"]) == 8
    row1 = next(x for x in data["rows"] if x["id"] == "case1")
    assert row1["p_value"] == pytest.approx(0.0082510259, rel=1e-6)
    assert math.isfinite(row1["lift"])
