#!/usr/bin/env python3
"""
Degenerate-Reporting Audit — Demo 11 student script.

Everything here is synthetic and offline: eight invented papers
(fixtures/papers.json) plus one anonymised teaching illustration
(fixtures/case_zero.json). No network, no credentials, no real publications.

Two reviewers read the same fixtures:

* NaiveReviewer  — accepts any paper whose reported attack-success rate
  after the defence is at most 5%. It takes claims at face value.
* RigorousAuditor — applies four deterministic checks before believing
  any number:

    R1  degenerate baseline present (always-allow / always-block /
        random / majority-class reported WITH scores)
    R2  base rate reported (else precision-style claims are unknowable)
    R3  recomputable (raw counts present) and powered (n >= 50)
    R4  metric sanity (the scoring rule must not reward doing nothing,
        e.g. abstention without a utility charge)

Verdicts: PASS (all checks hold), FAIL (a check fails),
INCONCLUSIVE (checks hold but evidence is too thin to rule anything out).
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FIXTURES = BASE_DIR / "fixtures"

DEGENERATE_BASELINES = ("always-allow", "always-block", "random", "majority-class")
MIN_POWERED_N = 50
NAIVE_ASR_THRESHOLD = 0.05


@dataclass
class Finding:
    rule: str
    passed: bool
    detail: str


@dataclass
class AuditVerdict:
    paper_id: str
    verdict: str  # PASS | FAIL | INCONCLUSIVE
    findings: list = field(default_factory=list)

    def reasons(self):
        return [f"{f.rule}: {f.detail}" for f in self.findings if not f.passed]


def load_papers():
    data = json.loads((FIXTURES / "papers.json").read_text())
    return data["papers"]


class NaiveReviewer:
    """Accepts any paper whose reported post-defence ASR is <= 5%."""

    def review(self, paper):
        asr_after = paper.get("asr_after")
        if asr_after is None:
            # No ASR reported at all: the naive reviewer falls back to any
            # headline number that looks good (here, reported accuracy).
            acc = paper.get("accuracy_reported")
            return acc is not None and acc >= 0.95
        return asr_after <= NAIVE_ASR_THRESHOLD


class RigorousAuditor:
    """Four deterministic checks. No judgement calls, no thresholds to tune."""

    def audit(self, paper):
        findings = [
            self._check_degenerate_baseline(paper),
            self._check_base_rate(paper),
            self._check_recomputable(paper),
            self._check_powered(paper),
            self._check_metric_sanity(paper),
        ]
        # R3a (raw counts) or R3b (small n) missing is INCONCLUSIVE;
        # anything else failing is FAIL.
        failed = [f for f in findings if not f.passed and f.rule not in ("R3a-counts", "R3b-power")]
        inconclusive = [f for f in findings if not f.passed and f.rule in ("R3a-counts", "R3b-power")]
        if failed:
            verdict = "FAIL"
        elif inconclusive:
            verdict = "INCONCLUSIVE"
        else:
            verdict = "PASS"
        return AuditVerdict(paper_id=paper["id"], verdict=verdict, findings=findings)

    def _check_degenerate_baseline(self, paper):
        reported = [b for b in paper.get("baselines_reported", []) if b in DEGENERATE_BASELINES]
        # 'no-defence' is the always-allow policy under a flattering name: it
        # is listed for transparency but does NOT satisfy R1 on its own,
        # because an evaluation that reports only the flattering baseline
        # cannot rule out a policy that merely denies more.
        if "no-defence" in paper.get("baselines_reported", []) and not reported:
            return Finding("R1-baseline", False,
                           "only the flattering 'no-defence' (always-allow) baseline; no unflattering baseline reported (lopsided reporting)")
        if not reported:
            return Finding("R1-baseline", False,
                           "no degenerate baseline reported: cannot rule out a do-nothing policy")
        # Majority-class listed without a reported score is decorative, and a
        # missing ASR-after means there is nothing to compare baselines against.
        if paper.get("asr_after") is None and "majority-class" in reported:
            return Finding("R1-baseline", False,
                           "majority-class listed but its score never reported and no post-defence ASR given: comparison is decorative")
        return Finding("R1-baseline", True, f"degenerate baselines reported: {', '.join(reported)}")

    def _check_base_rate(self, paper):
        if paper.get("base_rate_reported"):
            return Finding("R2-baserate", True, "base rate reported")
        return Finding("R2-baserate", False,
                       "no base rate: precision-style claims are unknowable without it")

    def _check_recomputable(self, paper):
        if paper.get("raw_counts"):
            return Finding("R3a-counts", True, "raw counts present")
        return Finding("R3a-counts", False,
                       "rates only, no raw counts: result cannot be recomputed or pooled")

    def _check_powered(self, paper):
        if paper.get("n_trials", 0) >= MIN_POWERED_N:
            return Finding("R3b-power", True, f"n={paper['n_trials']} >= {MIN_POWERED_N}")
        return Finding("R3b-power", False,
                       f"n={paper.get('n_trials')}: too small to rule out luck (underpowered, not wrong)")

    def _check_metric_sanity(self, paper):
        if paper.get("metric") == "abstention_rewarded_score":
            return Finding("R4-metric", False,
                           "scoring rule rewards abstention without charging lost utility: always-abstain scores as well as a perfect defence (degenerate metric)")
        return Finding("R4-metric", True, f"metric '{paper.get('metric')}' does not reward doing nothing")


def rescore_case_zero():
    """Rescore Case Study Zero verdicts against the sealed labels.

    Returns (reported_ranking, rescored_ranking, rows) where each ranking is
    a list of (policy, score) sorted best-first and rows hold per-item detail.
    """
    case = json.loads((FIXTURES / "case_zero.json").read_text())
    labels = case["sealed_labels"]
    item_ids = list(labels)
    reported = case["reported_verdicts"]

    def buggy_score(verdicts):
        # The published scorer: 'correct' whenever the policy said MALICIOUS.
        return sum(1 for v in verdicts if v == "malicious")

    def true_score(verdicts):
        return sum(1 for v, i in zip(verdicts, item_ids) if v == labels[i])

    reported_ranking = sorted(
        ((p, buggy_score(v) / len(item_ids)) for p, v in reported.items()),
        key=lambda t: t[1], reverse=True)
    rescored_ranking = sorted(
        ((p, true_score(v) / len(item_ids)) for p, v in reported.items()),
        key=lambda t: t[1], reverse=True)
    rows = [
        {"item": i, "sealed": labels[i],
         **{p: v[k] for p, v in reported.items()}}
        for k, i in enumerate(item_ids)
    ]
    return reported_ranking, rescored_ranking, rows


def main():
    papers = load_papers()
    naive = NaiveReviewer()
    auditor = RigorousAuditor()

    print(f"{'Paper':<6}{'Naive':<9}{'Audit':<14}Reason (first failing check)")
    print("-" * 78)
    for paper in papers:
        naive_says = "ACCEPT" if naive.review(paper) else "REJECT"
        verdict = auditor.audit(paper)
        first = verdict.reasons()[0] if verdict.reasons() else "all checks hold"
        print(f"{paper['id']:<6}{naive_says:<9}{verdict.verdict:<14}{first}")

    reported, rescored, _ = rescore_case_zero()
    print("\nCase Study Zero (anonymised teaching illustration):")
    print("  reported ranking: " + " > ".join(f"{p} ({s:.2f})" for p, s in reported))
    print("  rescored ranking: " + " > ".join(f"{p} ({s:.2f})" for p, s in rescored))
    if [p for p, _ in reported] != [p for p, _ in rescored]:
        print("  -> the ranking INVERTS once verdicts are scored against sealed labels")


if __name__ == "__main__":
    main()
