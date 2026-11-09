from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from coding import cohen_kappa, load, percent_agreement, validate_codebook


def data():
    return load(ROOT / "fixtures" / "codes.json")


def test_all_codes_in_codebook():
    assert validate_codebook(data()) == []


def test_agreement_is_four_of_six():
    assert percent_agreement(data()["documents"]) == round(4 / 6, 4)


def test_kappa_below_raw_agreement():
    d = data()
    pa = percent_agreement(d["documents"])
    kappa = cohen_kappa(d["documents"], d["codebook"])
    assert kappa < pa
    assert 0 < kappa < 1
