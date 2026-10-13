# Demo 45: Exact Nulls for Localisation Claims

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain why recall / precision / F1 at a fixed budget share one exact null
- Compute a hypergeometric upper-tail p-value for 8 synthetic localisation attempts
- Name the design limit (budget too small means nothing can clear alpha)
- Distinguish comparable null quantiles from incomparable ratio-to-null lifts

## Conceptual Explanation

A localisation claim says a method found the defective items at some budget.
At fixed pool `P`, defect count `D` and budget `k`, all three scores rise with
the same true-positive count, so every threshold event is `{TP >= t}` and the
null is hypergeometric — no resampling needed. On 8 hand-built cases:

| Case | Geometry P/D/k/TP | p-value | Verdict at 0.01 |
|------|-------------------|---------|-----------------|
| case1 | 45/10/8/5 | ~0.0083 | significant |
| case2 | 45/10/8/2 | chance-level | not significant |
| case5-transfer-A | 60/12/6/6 | ~1.8e-05 | significant |
| case6-transfer-B | 30/12/6/6 | ~0.0016 | significant but ~84x weaker |

The lesson: the two transfer cases share recall 0.50 yet live under different
nulls; their lifts (5.0 vs 2.5) are not comparable. Counting hits is the
measurement; the null decides what the count means.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real vulnerabilities, systems, or credentials
- No network access (standard library only)
- All cases and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real agents

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 45 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=45` |

## Research Connection

This demo illustrates the measurement question of an exact-null
localisation study. That measurement is
**pending**; every quantity there is `[RESULT PENDING]`. Nothing here
describes a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-45-localisation-nulls` (private research repo,
split from Demo-1 PR #4). It shares no topic with Demo 01 (BlindVerification):
Demo 01 seals *how* assessors commit; this demo tests *whether* a hit count
means anything.
