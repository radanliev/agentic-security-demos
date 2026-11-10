import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from erasure import exhaustive_min_erasure, greedy_erasure, score


def test_two_feature_flip():
    weights = [4.0, 0.1, 0.1, 0.1]
    x = [1.0, 1.0, 1.0, 1.0]
    bias = -0.2
    assert score(weights, x, bias) > 0
    idx, new = exhaustive_min_erasure(weights, x, bias)
    assert idx == [0, 1]
    assert new <= 0


def test_greedy_may_use_more_features():
    weights = [2.0, 1.0, 0.5, 0.1]
    x = [1.0, 1.0, 1.0, 1.0]
    ex, _ = exhaustive_min_erasure(weights, x, 0.0)
    gr, _ = greedy_erasure(weights, x, 0.0)
    assert ex is not None and gr is not None
    assert len(gr) >= len(ex)


def test_already_zero_needs_nothing():
    idx, value = exhaustive_min_erasure([1.0], [0.0], 0.0)
    assert idx == []
    assert value == 0.0


def test_run_writes_eight_rows():
    r = subprocess.run([sys.executable, "student/run_erasure.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert len(json.loads((ROOT / "results" / "erasure.json").read_text())["rows"]) == 8
