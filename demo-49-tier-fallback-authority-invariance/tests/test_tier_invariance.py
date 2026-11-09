import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from tier_invariance import ReferenceMonitor, check_trace, summarise  # noqa: E402

FIXTURE = json.loads((ROOT / "fixtures" / "synthetic_traces.json").read_text(encoding="utf-8"))
POLICY = FIXTURE["policy"]


class ReferenceMonitorTests(unittest.TestCase):
    def test_reference_monitor_trace_has_no_violations(self):
        m = ReferenceMonitor(policy=POLICY, task="intake_triage")
        m.propose("p1", "read_form")
        m.execute("p1", "read_form")
        m.propose("p2", "export_records")
        m.switch_tier("flash")
        m.execute("p2", "export_records")  # denied by policy on every tier
        m.propose("p3", "draft_reply")
        m.switch_tier("local")
        m.execute("p3", "draft_reply")  # re-validated after the switch
        self.assertEqual(check_trace(m.trace(), POLICY), [])

    def test_reference_monitor_decision_is_tier_independent(self):
        decisions = []
        for tier in ("frontier", "flash", "local"):
            m = ReferenceMonitor(policy=POLICY, task="intake_triage", tier=tier)
            m.propose("p1", "export_records")
            decisions.append(m.execute("p1", "export_records")["decision"])
        self.assertEqual(set(decisions), {"deny"})

    def test_unknown_tier_is_rejected(self):
        m = ReferenceMonitor(policy=POLICY, task="intake_triage")
        with self.assertRaises(ValueError):
            m.switch_tier("unlisted")


class CheckerTests(unittest.TestCase):
    def test_fixture_expectations(self):
        for trace in FIXTURE["traces"]:
            with self.subTest(trace=trace["name"]):
                rules = sorted({v.rule for v in check_trace(trace, POLICY)})
                self.assertEqual(rules, sorted(trace["expected_rules"]))

    def test_denied_step_after_switch_needs_no_revalidation(self):
        trace = {
            "task": "intake_triage",
            "steps": [
                {"step": 1, "tier": "frontier", "event": "propose", "plan_id": "p1", "action": "export_records"},
                {"step": 2, "tier": "flash", "event": "tier_switch"},
                {"step": 3, "tier": "flash", "event": "execute", "plan_id": "p1", "action": "export_records", "decision": "deny"},
            ],
        }
        self.assertEqual(check_trace(trace, POLICY), [])

    def test_malformed_step_is_reported(self):
        trace = {"task": "intake_triage", "steps": [{"step": 1, "tier": "edge", "event": "noop"}]}
        rules = [v.rule for v in check_trace(trace, POLICY)]
        self.assertEqual(rules, ["R0", "R0"])

    def test_summary_counts_each_rule_once_on_fixtures(self):
        counts = summarise(FIXTURE["traces"], POLICY)
        self.assertEqual(counts, {"R0": 0, "R1": 1, "R2": 1, "R3": 1})


if __name__ == "__main__":
    unittest.main()
