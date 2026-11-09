from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from power import load, plan_table, power_two_sample


def test_larger_effect_has_higher_power():
    assert power_two_sample(0.4, 1.0, 40) > power_two_sample(0.15, 1.0, 40)


def test_more_people_raise_power():
    assert power_two_sample(0.15, 1.0, 80) > power_two_sample(0.15, 1.0, 40)


def test_plan_table_matches_fixture():
    cfg = load(ROOT / "fixtures" / "plan.json")
    table = plan_table(cfg)
    assert table["immediate_power"] == power_two_sample(0.4, 1.0, 40)
    assert table["residual_power"] == power_two_sample(0.15, 1.0, 40)
    assert table["immediate_power"] > 0.4
    assert table["residual_power"] < table["immediate_power"]
