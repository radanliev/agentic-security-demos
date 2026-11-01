#!/usr/bin/env python3
"""Tests for Demo 31: Declaration Gap (teaching toy).

All verdicts are properties of synthetic fixtures, not research claims.
"""

import ast
import json
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_declarations import main  # noqa: E402
from declarations import check_all, least_declaration, gapped  # noqa: E402

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

EXPECTED_GAPPED = ["i1", "i4", "i5", "i6", "i8"]
EXPECTED_TIGHT = ["i2", "i3", "i7"]

REQUIRED_RESULT_KEYS = {
    "demo",
    "experiment",
    "seed",
    "total",
    "gapped",
    "gapped_ids",
    "least_declaration",
    "rows",
    "notes",
}


def load_pack() -> dict:
    """Load the synthetic fixture pack."""
    return json.loads((DEMO_DIR / "fixtures" / "declarations.json").read_text())


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_declarations.py")],
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


def test_fixture_rows_have_declared_and_exercised_lists():
    """Every row carries non-empty declared and exercised authority lists."""
    for integration in load_pack()["integrations"]:
        assert isinstance(integration["declared"], list)
        assert isinstance(integration["exercised"], list)
        assert integration["declared"] and integration["exercised"]


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
    assert "gapped 5/8  least-declaration 8 authority items" in proc.stdout
    assert "least: calendar.read,chat,drive.read,drive.write,files.read,read,repo,write" in proc.stdout


# --- Declaration gap verdicts ---


def test_five_of_eight_gapped():
    """Five of eight integrations have a declaration gap."""
    out = main()
    assert out["total"] == 8
    assert out["gapped"] == 5
    assert out["gapped_ids"] == ["i1", "i4", "i5", "i6", "i8"]


def test_gapped_ids_exact():
    """The gapped set is exactly the five gap cases."""
    pack = load_pack()
    assert check_all(pack["integrations"])["over"] == EXPECTED_GAPPED


def test_tight_ids_exact():
    """Equal declared/exercised rows are tight: i2, i3, i7."""
    pack = load_pack()
    assert check_all(pack["integrations"])["tight"] == EXPECTED_TIGHT


def test_i1_admin_gap_case():
    """i1 declares admin it never exercises: the classic gap case."""
    pack = load_pack()
    i1 = next(i for i in pack["integrations"] if i["id"] == "i1")
    assert "admin" in set(i1["declared"]) - set(i1["exercised"])
    assert gapped(i1) is True


def test_i8_drive_admin_gap_case():
    """i8 declares drive.admin it never exercises."""
    pack = load_pack()
    i8 = next(i for i in pack["integrations"] if i["id"] == "i8")
    assert "drive.admin" in set(i8["declared"]) - set(i8["exercised"])
    assert gapped(i8) is True


# --- Union rule ---


def test_least_declaration_union():
    """Least-declaration set is the sorted union of exercised authority."""
    pack = json.loads((DEMO_DIR / "fixtures" / "declarations.json").read_text())
    assert least_declaration(pack["integrations"]) == EXPECTED_LEAST
    out = main()
    assert out["least_declaration"] == EXPECTED_LEAST


def test_least_declaration_is_sorted_set_union():
    """The union is sorted and equals the set union of all exercised authority."""
    pack = load_pack()
    union = least_declaration(pack["integrations"])
    expected = set()
    for integration in pack["integrations"]:
        expected.update(integration["exercised"])
    assert union == sorted(expected)
    assert len(union) == 8


# --- Strict-superset rule ---


def test_strict_superset_rule():
    """Equal declared/exercised is tight; strict superset is gapped."""
    assert gapped({"declared": ["read"], "exercised": ["read"]}) is False
    assert gapped({"declared": ["read", "write"], "exercised": ["read"]}) is True
    assert gapped({"declared": ["read"], "exercised": ["read", "write"]}) is False


def test_empty_exercised_with_declare_is_gapped():
    """Declaring authority while exercising none is gapped."""
    assert gapped({"declared": ["read"], "exercised": []}) is True


def test_empty_declared_is_tight():
    """Declaring nothing cannot be gapped."""
    assert gapped({"declared": [], "exercised": []}) is False


def test_exercising_more_does_not_close_gap():
    """Adding exercised authority to declared still leaves excess declared."""
    assert gapped({"declared": ["read", "write", "admin"], "exercised": ["read", "admin"]}) is True


# --- Parity, seed, schema ---


def test_results_file_matches_memory():
    """Results on disk equal the in-memory evaluation."""
    out = main()
    on_disk = json.loads((DEMO_DIR / "results" / "declarations.json").read_text())
    assert on_disk == out
    assert on_disk["notes"] == "Synthetic teaching fixture"
    assert on_disk["seed"] == 31


def test_results_schema_has_required_keys():
    """The results file follows the standardized result schema."""
    out = main()
    assert REQUIRED_RESULT_KEYS <= set(out)
    assert out["demo"] == "demo-31-declaration-gap"
    assert out["experiment"] == "declaration-gap"
    assert len(out["rows"]) == out["total"] == 8


def test_check_all_partitions_every_id():
    """Gapped plus tight ids partition the fixture without overlap."""
    pack = load_pack()
    summary = check_all(pack["integrations"])
    assert sorted(summary["over"] + summary["tight"]) == [f"i{n}" for n in range(1, 9)]
    assert not set(summary["over"]) & set(summary["tight"])


def test_student_code_is_stdlib_only():
    """Student helpers import only the standard library (offline demo)."""
    allowed = set(sys.stdlib_module_names)
    local = {p.stem for p in (DEMO_DIR / "student").glob("*.py")}
    for name in ("declarations.py", "run_declarations.py"):
        tree = ast.parse((DEMO_DIR / "student" / name).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    assert top in allowed or top in local, f"{name}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                top = (node.module or "").split(".")[0]
                assert top in allowed or top in local, f"{name}: {node.module}"
