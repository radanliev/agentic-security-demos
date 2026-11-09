import json
import pathlib
import random
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from delegation_budget import BudgetLedger, replay, requested_spend  # noqa: E402

FIXTURE = json.loads((ROOT / "fixtures" / "synthetic_plans.json").read_text(encoding="utf-8"))


class FixtureTests(unittest.TestCase):
    def test_fixture_expectations(self):
        for plan in FIXTURE["plans"]:
            with self.subTest(plan=plan["name"]):
                ledger = replay(plan)
                self.assertEqual(len(ledger.denials()), plan["expected_denials"])
                self.assertEqual(ledger.total_spent(), plan["expected_total_spent"])
                self.assertEqual(requested_spend(plan), plan["expected_requested_spend"])
                self.assertTrue(all(ledger.audit().values()), ledger.audit())

    def test_denial_reasons_on_fixtures(self):
        reasons = {
            plan["name"]: sorted(d.reason for d in replay(plan).denials()) for plan in FIXTURE["plans"]
        }
        self.assertEqual(reasons["within_budget"], [])
        self.assertEqual(reasons["fanout_beyond_cap"], ["fan-out cap", "fan-out cap", "unknown node", "unknown node"])
        self.assertEqual(reasons["chain_beyond_depth"], ["depth cap", "unknown node"])
        self.assertEqual(
            reasons["overspend_request"], ["exceeds parent's remaining budget", "exceeds remaining budget"]
        )


class LedgerTests(unittest.TestCase):
    def test_partial_grant_when_enabled(self):
        ledger = BudgetLedger("root", 1000, max_depth=1, max_fanout=1, allow_partial=True)
        decision = ledger.delegate("root", "child", 1500)
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.granted, 1000)
        self.assertEqual(decision.reason, "granted in part")
        self.assertEqual(ledger.nodes["root"].remaining, 0)

    def test_negative_limits_rejected(self):
        with self.assertRaises(ValueError):
            BudgetLedger("root", -1, 1, 1)

    def test_invariants_hold_on_random_plans(self):
        rng = random.Random(7)
        for _ in range(300):
            ledger = BudgetLedger("root", rng.randint(0, 5000), rng.randint(0, 4), rng.randint(0, 4))
            names = ["root"]
            for i in range(rng.randint(1, 40)):
                if rng.random() < 0.5:
                    child = f"n{i}"
                    ledger.delegate(rng.choice(names + ["ghost"]), child, rng.randint(-50, 3000))
                    names.append(child)
                else:
                    ledger.spend(rng.choice(names + ["ghost"]), rng.randint(-50, 3000))
            audit = ledger.audit()
            self.assertTrue(all(audit.values()), audit)
            self.assertLessEqual(ledger.total_spent(), ledger.root_budget)


if __name__ == "__main__":
    unittest.main()
