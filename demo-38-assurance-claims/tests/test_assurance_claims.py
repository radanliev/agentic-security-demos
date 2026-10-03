#!/usr/bin/env python3
"""Tests for Demo 38: Assurance Claims (teaching toy).

All verdicts are properties of the hand-built synthetic fixture
(fixtures/cards8.json), not research claims. Nothing here measures real
system cards. The research study this demo illustrates is pending and every
quantity there is [RESULT PENDING].
"""

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))
from run_claims import main  # noqa: E402
from claims import coverage  # noqa: E402

FORBIDDEN_IMPORTS = ("socket", "requests", "urllib", "aiohttp", "httpx")

EXPECTED_PER_OBLIGATION = {
    "threats": 7,
    "evals": 5,
    "agentic": 4,
    "third_party": 2,
    "mitigations": 7,
}
EXPECTED_OBLIGATIONS = ["threats", "evals", "agentic", "third_party", "mitigations"]


def run_demo() -> subprocess.CompletedProcess:
    """Run the evaluator as a subprocess for determinism checks."""
    return subprocess.run(
        [sys.executable, str(DEMO_DIR / "student" / "run_claims.py")],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )


def fixture_pack() -> dict:
    """Load the synthetic card pack."""
    return json.loads((DEMO_DIR / "fixtures" / "cards8.json").read_text())


class TestFixtureIntegrity:
    """The hand-built fixture has exactly 8 cards over 5 obligations."""

    def test_fixture_has_eight_cards_five_obligations(self):
        """Pack holds 8 cards, 5 obligations, seed 38."""
        pack = fixture_pack()
        assert len(pack["cards"]) == 8
        assert pack["obligations"] == EXPECTED_OBLIGATIONS
        assert pack["seed"] == 38

    def test_fixture_cards_have_required_keys(self):
        """Every card carries an id and a boolean per obligation."""
        pack = fixture_pack()
        for card in pack["cards"]:
            assert isinstance(card["id"], str) and card["id"]
            for ob in pack["obligations"]:
                assert isinstance(card[ob], bool), f"{card['id']}.{ob} is not boolean"

    def test_fixture_ids_unique(self):
        """Card ids are unique (coverage counts cards, not rows)."""
        pack = fixture_pack()
        ids = [c["id"] for c in pack["cards"]]
        assert len(set(ids)) == 8


class TestDeterminism:
    """Same input gives same output, in-process and across processes."""

    def test_eval_is_deterministic(self):
        """Two subprocess runs print identical output."""
        first = run_demo()
        second = run_demo()
        assert first.returncode == 0 and second.returncode == 0
        assert first.stdout == second.stdout

    def test_coverage_is_pure_function(self):
        """Two in-memory calls on the same pack agree exactly."""
        pack = fixture_pack()
        assert coverage(pack["cards"], pack["obligations"]) == coverage(
            pack["cards"], pack["obligations"]
        )


class TestCoverageTallies:
    """Hand-picked tallies: full coverage 2/8, weakest third_party 2/8."""

    def test_full_coverage_and_weakest(self):
        """2/8 cards cover every obligation; weakest is third_party at 2/8."""
        pack = fixture_pack()
        cov = coverage(pack["cards"], pack["obligations"])
        assert cov["n"] == 8
        assert cov["full_coverage"] == 2
        assert cov["weakest"] == "third_party"
        assert cov["weakest_count"] == 2

    def test_per_obligation_counts(self):
        """Hand-picked per-obligation tallies hold exactly."""
        pack = fixture_pack()
        cov = coverage(pack["cards"], pack["obligations"])
        assert cov["per_obligation"] == EXPECTED_PER_OBLIGATION

    def test_full_coverage_cards_are_card1_card2(self):
        """Only card1 and card2 set every obligation flag."""
        pack = fixture_pack()
        full = [
            c["id"]
            for c in pack["cards"]
            if all(c.get(ob, False) for ob in pack["obligations"])
        ]
        assert full == ["card1", "card2"]

    def test_each_obligation_count_matches_independent_recount(self):
        """Tallies match a naive independent recount (no shared code path)."""
        pack = fixture_pack()
        cov = coverage(pack["cards"], pack["obligations"])
        for ob in pack["obligations"]:
            assert cov["per_obligation"][ob] == len(
                [c for c in pack["cards"] if c[ob] is True]
            )

    def test_single_card_flip_moves_full_coverage_not_weakest(self):
        """Hand-built experiment: card3 gaining third_party moves full 2/8 to
        3/8 while the weakest link stays third_party (now 3/8)."""
        pack = fixture_pack()
        cards = [dict(c) for c in pack["cards"]]
        cards[2] = dict(cards[2], third_party=True)
        cov = coverage(cards, pack["obligations"])
        assert cov["full_coverage"] == 3
        assert cov["weakest"] == "third_party"
        assert cov["weakest_count"] == 3


class TestParityAndSeed:
    """Results on disk equal the in-memory evaluation; seed and notes fixed."""

    def test_results_file_matches_memory(self):
        """Results on disk equal the in-memory evaluation."""
        out = main()
        on_disk = json.loads((DEMO_DIR / "results" / "claims.json").read_text())
        assert on_disk == out
        assert on_disk["notes"] == "Synthetic teaching fixture"
        assert on_disk["seed"] == 38

    def test_run_claims_exit_zero_and_prints_table(self):
        """The evaluator exits 0 and prints the verbatim coverage table."""
        proc = run_demo()
        assert proc.returncode == 0, proc.stderr
        assert "cards 8  obligations 5" in proc.stdout
        assert "full coverage 2/8" in proc.stdout
        assert "weakest: third_party (2/8)." in proc.stdout


class TestStdlibOnly:
    """Student modules use no network or third-party imports."""

    def test_stdlib_only(self):
        """Student modules use no network imports."""
        for module in ("claims.py", "run_claims.py"):
            src = (DEMO_DIR / "student" / module).read_text()
            for marker in FORBIDDEN_IMPORTS:
                assert marker not in src, f"{module} uses forbidden import ({marker})"

    def test_imports_are_stdlib_or_local(self):
        """AST check: every import resolves to stdlib or the sibling module."""
        allowed = {
            "json", "sys", "pathlib", "argparse", "hashlib", "csv", "re",
            "os", "platform", "subprocess", "claims",
        }
        for module in ("claims.py", "run_claims.py"):
            tree = ast.parse((DEMO_DIR / "student" / module).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert alias.name.split(".")[0] in allowed, module
                elif isinstance(node, ast.ImportFrom):
                    assert (node.module or "").split(".")[0] in allowed, module


class TestResultsSchema:
    """results/claims.json follows the standard result schema."""

    def test_results_schema(self):
        """Top-level keys: demo, experiment, seed, obligations, coverage, notes."""
        out = main()
        assert out["demo"] == "demo-38-assurance-claims"
        assert out["experiment"] == "assurance-coverage"
        assert isinstance(out["seed"], int)
        assert out["obligations"] == EXPECTED_OBLIGATIONS
        assert isinstance(out["coverage"], dict)
        assert isinstance(out["notes"], str)

    def test_coverage_schema(self):
        """Coverage block carries n, per-obligation counts, full tally, weakest."""
        out = main()
        cov = out["coverage"]
        assert cov["n"] == 8
        assert set(cov["per_obligation"]) == set(EXPECTED_OBLIGATIONS)
        assert all(isinstance(v, int) for v in cov["per_obligation"].values())
        assert isinstance(cov["full_coverage"], int)
        assert cov["weakest"] in EXPECTED_OBLIGATIONS
        assert cov["weakest_count"] == cov["per_obligation"][cov["weakest"]]

    def test_weakest_tiebreak_is_deterministic(self):
        """Ties break identically on every run (no dict-order dependence)."""
        pack = fixture_pack()
        first = coverage(pack["cards"], pack["obligations"])["weakest"]
        for _ in range(5):
            assert coverage(pack["cards"], pack["obligations"])["weakest"] == first

    def test_all_false_pack_weakest_is_alphabetical_first(self):
        """A total tie (every count 0) breaks alphabetically, deterministically."""
        pack = fixture_pack()
        cards = [{**c, **{ob: False for ob in pack["obligations"]}} for c in pack["cards"]]
        cov = coverage(cards, pack["obligations"])
        assert cov["full_coverage"] == 0
        assert cov["weakest"] == min(pack["obligations"])
        assert cov["weakest_count"] == 0

    def test_empty_card_list_yields_zeroes(self):
        """Edge case: no cards gives n=0 and zero tallies without crashing."""
        pack = fixture_pack()
        cov = coverage([], pack["obligations"])
        assert cov["n"] == 0
        assert cov["full_coverage"] == 0
        assert all(v == 0 for v in cov["per_obligation"].values())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
