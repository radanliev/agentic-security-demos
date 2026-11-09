from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from validate import coverage, design_based_error_rate, load, planted


def data():
    return load(ROOT / "fixtures" / "outputs.json")


def test_three_planted_errors():
    assert len(planted(data()["items"])) == 3


def test_sample_catches_all_planted():
    d = data()
    cov = coverage(d["items"], d["sample_ids"])
    assert cov["planted_in_sample"] == 3
    assert cov["coverage"] == 1.0


def test_sample_error_rate():
    d = data()
    # sample is a2 (err), a4 (ok), a5 (err), a8 (err) -> 3/4
    assert design_based_error_rate(d["items"], d["sample_ids"]) == 0.75
