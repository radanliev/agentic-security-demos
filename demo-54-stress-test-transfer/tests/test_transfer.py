from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from transfer import evaluate, load, transfer_gap


def data():
    return load(ROOT / "fixtures" / "cases.json")


def test_in_distribution_is_perfect():
    d = data()
    ev = evaluate(d["in_distribution"], d["threshold"])
    assert ev["recall"] == 1.0
    assert ev["accuracy"] == 1.0
    assert ev["missed_attacks"] == 0


def test_shifted_misses_both_attacks():
    d = data()
    ev = evaluate(d["shifted"], d["threshold"])
    assert ev["recall"] == 0.0
    assert ev["missed_attacks"] == 2
    assert ev["false_positive_rate"] == 0.0


def test_recall_drops():
    d = data()
    ind = evaluate(d["in_distribution"], d["threshold"])
    sh = evaluate(d["shifted"], d["threshold"])
    assert transfer_gap(ind, sh)["recall_drop"] == 1.0
