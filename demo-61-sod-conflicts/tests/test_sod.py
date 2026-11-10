import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "student"))
from sod import audit, conflicts_for, effective_permissions


def _data():
    return json.loads((ROOT / "fixtures" / "policies.json").read_text())


def test_teller_has_no_sod_pair():
    data = _data()
    assert conflicts_for("u1", data["role_members"], data["role_permissions"], data["constraints"]) == []


def test_dual_role_is_gapped():
    data = _data()
    found = conflicts_for("u8", data["role_members"], data["role_permissions"], data["constraints"])
    assert ["post_payment", "approve_payment"] in found


def test_effective_union():
    data = _data()
    assert effective_permissions("u8", data["role_members"], data["role_permissions"]) == {"post_payment", "approve_payment"}


def test_audit_counts():
    data = _data()
    rows = audit(data["users"], data["role_members"], data["role_permissions"], data["constraints"])
    assert len(rows) == 8
    assert sum(1 for row in rows if row["gapped"]) == 1


def test_run_writes_results():
    r = subprocess.run([sys.executable, "student/run_sod.py"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads((ROOT / "results" / "sod.json").read_text())["gapped"] == ["u8"]
