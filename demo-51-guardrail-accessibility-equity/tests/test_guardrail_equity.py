import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from guardrail_equity import disparity, fit_thresholds, paired_flip_rate, rates  # noqa: E402

FIXTURE = json.loads((ROOT / "fixtures" / "synthetic_scores.json").read_text(encoding="utf-8"))
RECORDS = FIXTURE["records"]
GLOBAL = FIXTURE["global_threshold"]


class AuditTests(unittest.TestCase):
    def test_rates_at_global_threshold(self):
        table = rates(RECORDS, GLOBAL)
        fpr = {v: row["fpr"] for v, row in table.items()}
        self.assertEqual(
            fpr,
            {
                "standard": 0.0,
                "speech_to_text": 0.5,
                "dyslexia_pattern_spelling": 0.5,
                "aac_telegraphic": 0.75,
                "plain_language": 0.25,
            },
        )
        self.assertTrue(all(row["tpr"] == 1.0 for row in table.values()))

    def test_smoothed_disparity_against_reference(self):
        ratios = disparity(rates(RECORDS, GLOBAL))
        expected = {
            "standard": 1.0,
            "speech_to_text": 5.0,
            "dyslexia_pattern_spelling": 5.0,
            "aac_telegraphic": 7.0,
            "plain_language": 3.0,
        }
        for variant, value in expected.items():
            self.assertAlmostEqual(ratios[variant], value, places=9)

    def test_paired_flip_rate(self):
        flips = paired_flip_rate(RECORDS, GLOBAL)
        self.assertEqual(
            flips,
            {"speech_to_text": 0.5, "dyslexia_pattern_spelling": 0.5, "aac_telegraphic": 0.75, "plain_language": 0.25},
        )

    def test_audit_threshold_fit_and_conflict(self):
        thresholds, conflicts = fit_thresholds(RECORDS, GLOBAL, target_fpr=0.25, recall_floor=0.9)
        self.assertEqual(
            thresholds,
            {
                "aac_telegraphic": 0.5,
                "dyslexia_pattern_spelling": 0.70,
                "plain_language": 0.58,
                "speech_to_text": 0.60,
                "standard": 0.5,
            },
        )
        self.assertEqual(conflicts, ["aac_telegraphic"])

    def test_fit_is_never_stricter_than_global(self):
        thresholds, _ = fit_thresholds(RECORDS, GLOBAL, target_fpr=0.25, recall_floor=0.9)
        self.assertTrue(all(t >= GLOBAL for t in thresholds.values()))

    def test_fitted_rates_respect_target_except_conflicts(self):
        thresholds, conflicts = fit_thresholds(RECORDS, GLOBAL, target_fpr=0.25, recall_floor=0.9)
        table = rates(RECORDS, thresholds)
        for variant, row in table.items():
            if variant in conflicts:
                continue
            self.assertLessEqual(row["fpr"], 0.25)
            self.assertGreaterEqual(row["tpr"], 0.9)

    def test_unknown_label_is_rejected(self):
        with self.assertRaises(ValueError):
            rates([{"variant": "standard", "label": "unclear", "score": 0.4}], GLOBAL)


if __name__ == "__main__":
    unittest.main()
