# Demo 11: Degenerate Reporting

## Learning Objectives

- Explain why an evaluation without a degenerate (do-nothing) baseline proves nothing about a defence
- Distinguish flattering baselines ("no defence") from unflattering ones (always-block, random, majority-class)
- Show why accuracy-style claims are unknowable without base rates and raw counts
- Detect metrics that reward doing nothing (e.g. abstention without a utility charge)
- Rescore published verdicts against sealed labels and watch a ranking invert

## Conceptual Explanation

**Degenerate reporting** is an evaluation failure mode: a defence paper reports numbers that a trivial, do-nothing policy could also produce — and never runs the trivial policy, so nobody notices.

A **degenerate (do-nothing) baseline** is a policy with no intelligence in it: `always-allow` admits everything, `always-block` denies everything, `random` decides by coin flip, `majority-class` always predicts the common class. If a paper reports none of these *with scores*, its headline number floats free: a 0.03 attack-success rate means nothing if always-allowing everything also scores 0.03 on the same trials.

The demo's rigorous auditor applies four deterministic checks — degenerate baseline present (R1), base rate reported (R2), recomputable with adequate power (R3), metric sanity (R4) — to eight synthetic papers. It passes 2 of 8; a naive headline-reader accepts 7 of 8. A final anonymised case study shows a scorer that equated "verdict correct" with "said MALICIOUS": rescoring against sealed labels inverts the published ranking.

## Safety Notice

⚠️ **Teaching demonstration only.**
- **All eight "papers" are invented** — titles, numbers and verdicts describe no real publication
- Case Study Zero is anonymised and fully synthetic; it names no system, author, or venue
- No network access, no credentials, no real paper titles

## Run It

```bash
cd demo-11-degenerate-reporting
python3 -m pytest tests/ -v          # 23 tests, ~1 min
python3 student/audit_reporting.py   # both reviewers + case rescore
python3 student/generate_audit_results.py  # writes results/audit_results.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-11-degenerate-reporting/INSTRUCTIONS.md). Course lab: [Lab 11](../course/lab-11-degenerate-reporting.md).
