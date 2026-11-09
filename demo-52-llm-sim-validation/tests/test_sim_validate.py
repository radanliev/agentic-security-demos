from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from sim_validate import contamination_probe, honest_predict, load_cohorts, memorizer_predict, score_heldout


def data():
    return load_cohorts(ROOT / "fixtures" / "cohorts.json")


def test_honest_beats_memorizer_on_unseen_module():
    d = data()
    honest = score_heldout(honest_predict, d["train_modules"], d["heldout_modules"])
    memo = score_heldout(memorizer_predict, d["train_modules"], d["heldout_modules"])
    assert honest["pass_mae"] < memo["pass_mae"]


def test_honest_transfers_under_rename():
    d = data()
    probe = contamination_probe(honest_predict, d["train_modules"], d["renamed_probe"])
    assert probe["failed_to_transfer"] is False
    assert probe["predicted_pass"] == 0.62


def test_memorizer_fails_rename_probe():
    d = data()
    probe = contamination_probe(memorizer_predict, d["train_modules"], d["renamed_probe"])
    assert probe["failed_to_transfer"] is True
    assert probe["source"] == "unknown-name"
