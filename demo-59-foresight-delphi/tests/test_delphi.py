from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from delphi import load, median, summarise


def data():
    return load(ROOT / "fixtures" / "ratings.json")


def test_p1_has_tight_consensus():
    p1 = next(p for p in data()["propositions"] if p["id"] == "P1")
    row = summarise(p1)
    assert row["median"] == 6.0
    assert row["consensus"] is True


def test_p2_is_split_by_an_outlier():
    p2 = next(p for p in data()["propositions"] if p["id"] == "P2")
    row = summarise(p2)
    assert row["consensus"] is False
    assert row["iqr"] > 1.5


def test_median_of_odd_list():
    assert median([2, 3, 2, 7, 3]) == 3
