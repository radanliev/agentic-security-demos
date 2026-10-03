#!/usr/bin/env python3
"""Tests for Demo 31: Scope Creep (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import ast
import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_scopes import main  # noqa: E402
from scopes import check_all, least_privilege, overprivileged  # noqa: E402

EXPECTED_LEAST = [
    "calendar.read",
    "chat",
    "drive.read",
    "drive.write",
    "files.read",
    "read",
    "repo",
    "write",
]

EXPECTED_OVER = ["i1", "i4", "i5", "i6", "i8"]
EXPECTED_TIGHT = ["i2", "i3", "i7"]

REQUIRED_RESULT_KEYS = {
    "demo",
    "experiment",
    "seed",
    "total",
    "overprivileged",
    "overprivileged_ids",
    "least_privilege",
    "rows",
    "notes",
}


def load_pack() -> dict:
    """Load the synthetic fixture pack."""
    return json.loads((DEMO_DIR / "fixtures" / "integrations.json").read_text())


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_scopes.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


# --- Fixture integrity ---


def test_fixture_has_eight_integrations():
    """The fixture holds exactly eight hand-built integrations."""
    pack = load_pack()
    assert len(pack["integrations"]) == 8


def test_fixture_ids_are_unique_cover_i1_to_i8():
    """Integration ids are unique and exactly i1..i8."""
    pack = load_pack()
    ids = [i["id"] for i in pack["integrations"]]
    assert sorted(ids) == [f"i{n}" for n in range(1, 9)]


def test_fixture_seed_is_31():
    """The fixture seed is fixed at 31."""
    assert load_pack()["seed"] == 31


def test_fixture_rows_have_requested_and_used_lists():
    """Every row carries non-empty requested and used scope lists."""
    for integration in load_pack()["integrations"]:
        assert isinstance(integration["requested"], list)
        assert isinstance(integration["used"], list)
        assert integration["requested"] and integration["used"]


# --- Determinism ---


def test_eval_is_deterministic():
    """Two runs print identical output."""
    first = run_demo()
    second = run_demo()
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout


def test_subprocess_output_matches_expected_table():
    """The printed table matches the hand-built expectation verbatim."""
    proc = run_demo()
    assert "over-privileged 5/8  least-privilege 8 scopes" in proc.stdout
    assert "least: calendar.read,chat,drive.read,drive.write,files.read,read,repo,write" in proc.stdout


# --- Over-privilege verdicts ---


def test_five_of_eight_overprivileged():
    """Five of eight integrations are over-privileged."""
    out = main()
    assert out["total"] == 8
    assert out["overprivileged"] == 5
    assert out["overprivileged_ids"] == ["i1", "i4", "i5", "i6", "i8"]


def test_overprivileged_ids_exact():
    """The over-privileged set is exactly the five creep cases."""
    pack = load_pack()
    assert check_all(pack["integrations"])["over"] == EXPECTED_OVER


def test_tight_ids_exact():
    """Equal requested/used rows are tight: i2, i3, i7."""
    pack = load_pack()
    assert check_all(pack["integrations"])["tight"] == EXPECTED_TIGHT


def test_i1_admin_creep_case():
    """i1 requests admin it never uses: the classic creep case."""
    pack = load_pack()
    i1 = next(i for i in pack["integrations"] if i["id"] == "i1")
    assert "admin" in set(i1["requested"]) - set(i1["used"])
    assert overprivileged(i1) is True


def test_i8_drive_admin_creep_case():
    """i8 requests drive.admin it never uses."""
    pack = load_pack()
    i8 = next(i for i in pack["integrations"] if i["id"] == "i8")
    assert "drive.admin" in set(i8["requested"]) - set(i8["used"])
    assert overprivileged(i8) is True


# --- Union rule ---


def test_least_privilege_union():
    """Least-privilege set is the sorted union of used scopes."""
    pack = json.loads((DEMO_DIR / "fixtures" / "integrations.json").read_text())
    assert least_privilege(pack["integrations"]) == EXPECTED_LEAST
    out = main()
    assert out["least_privilege"] == EXPECTED_LEAST


def test_least_privilege_is_sorted_set_union():
    """The union is sorted and equals the set union of all used scopes."""
    pack = load_pack()
    union = least_privilege(pack["integrations"])
    expected = set()
    for integration in pack["integrations"]:
        expected.update(integration["used"])
    assert union == sorted(expected)
    assert len(union) == 8


# --- Strict-superset rule ---


def test_strict_superset_rule():
    """Equal requested/used is tight; strict superset is over."""
    assert overprivileged({"requested": ["read"], "used": ["read"]}) is False
    assert overprivileged({"requested": ["read", "write"], "used": ["read"]}) is True
    assert overprivileged({"requested": ["read"], "used": ["read", "write"]}) is False


def test_empty_used_with_request_is_overprivileged():
    """Requesting scopes while using none is over-privileged."""
    assert overprivileged({"requested": ["read"], "used": []}) is True


def test_empty_requested_is_tight():
    """Requesting nothing cannot be over-privileged."""
    assert overprivileged({"requested": [], "used": []}) is False


def test_using_more_does_not_fix_creep():
    """Adding an unused scope to used still leaves excess requested."""
    assert overprivileged({"requested": ["read", "write", "admin"], "used": ["read", "admin"]}) is True


# --- Parity, seed, schema ---


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "scopes.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 31


def test_results_schema_has_required_keys():
    """The results file follows the standardized result schema."""
    out = main()
    assert REQUIRED_RESULT_KEYS <= set(out)
    assert out["demo"] == "demo-31-scope-creep"
    assert out["experiment"] == "scope-creep"
    assert len(out["rows"]) == out["total"] == 8


def test_check_all_partitions_every_id():
    """Over-privileged plus tight ids partition the fixture without overlap."""
    pack = load_pack()
    summary = check_all(pack["integrations"])
    assert sorted(summary["over"] + summary["tight"]) == [f"i{n}" for n in range(1, 9)]
    assert not set(summary["over"]) & set(summary["tight"])


def test_student_code_is_stdlib_only():
    """Student helpers import only the standard library (offline demo)."""
    allowed = set(sys.stdlib_module_names)
    local = {p.stem for p in (DEMO_DIR / "student").glob("*.py")}
    for name in ("scopes.py", "run_scopes.py"):
        tree = ast.parse((DEMO_DIR / "student" / name).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    assert top in allowed or top in local, f"{name}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                top = (node.module or "").split(".")[0]
                assert top in allowed or top in local, f"{name}: {node.module}"
