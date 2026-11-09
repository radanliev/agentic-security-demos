from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from battery import load, peak_time, score_battery, growth_label, construct_ok


def data():
    return load(ROOT / "fixtures" / "tasks.json")["tasks"]


def test_peak_is_at_time_two():
    assert peak_time([0.1, 0.4, 1.8, 0.5, 0.2], [0, 1, 2, 3, 4]) == 2


def test_flat_growth():
    assert growth_label([1.0, 1.1, 1.0, 1.05, 0.98]) == "flat"


def test_construct_has_all_parts():
    assert construct_ok("PROM-RBS-GENE-TERM", ["PROM", "RBS", "GENE", "TERM"]) is True


def test_battery_is_all_correct():
    report = score_battery(data())
    assert report["n"] == 3
    assert report["accuracy"] == 1.0
