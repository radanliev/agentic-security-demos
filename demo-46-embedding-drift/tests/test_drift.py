import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from drift import cosine, shift  # noqa: E402


def test_identical_is_zero_shift():
    assert shift([1, 2, 3], [1, 2, 3]) == 0.0
    assert cosine([1, 0], [1, 0]) == 1.0


def test_orthogonal_shift_is_one():
    assert shift([1, 0], [0, 1]) == pytest_approx_one()


def pytest_approx_one():
    return 1.0


def test_known_small_shift():
    value = shift([1, 0, 0, 0], [0.98, 0.2, 0, 0])
    expect = 1 - (0.98 / math.sqrt(0.98 ** 2 + 0.2 ** 2))
    assert value == expect


def test_demo_flags_orthogonal_only():
    subprocess.check_call([sys.executable, "student/run_drift.py"], cwd=ROOT)
    data = json.loads((ROOT / "results" / "drift.json").read_text())
    flags = {row["id"]: row["above_frozen_mean"] for row in data["cases"]}
    assert flags == {"small": False, "orthogonal": True}
    assert data["frozen_mean_cosine_shift"] == 0.1222
