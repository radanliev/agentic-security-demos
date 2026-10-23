# Demo 45: Exact Nulls

## Learning Objectives

- Explain why recall / precision / F1 at a fixed budget share one exact null
- Compute a hypergeometric upper-tail p-value for 8 synthetic localisation attempts
- Name the design limit (budget too small means nothing can clear alpha)
- Distinguish comparable null quantiles from incomparable ratio-to-null lifts

## Conceptual Explanation

A localisation claim says a method found the defective items at some budget. At fixed pool `P`, defect count `D` and budget `k`, all three scores rise with the same true-positive count, so every threshold event is `{TP >= t}` and the null is hypergeometric — no resampling needed. On 8 hand-built cases:

| Case | Geometry P/D/k/TP | p-value | Verdict at 0.01 |
|------|-------------------|---------|-----------------|
| case1 | 45/10/8/5 | ~0.0083 | significant |
| case2 | 45/10/8/2 | chance-level | not significant |
| case5-transfer-A | 60/12/6/6 | ~1.8e-05 | significant |
| case6-transfer-B | 30/12/6/6 | ~0.0016 | significant but ~84x weaker |

The lesson: the two transfer cases share recall 0.50 yet live under different nulls; their lifts (5.0 vs 2.5) are not comparable. Counting hits is the measurement; the null decides what the count means.

Boundary: this demo computes exact nulls for localisation counts; it is not the seal-before-reveal mechanism (Demo 47). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real vulnerabilities, systems, or credentials
- No network access (standard library only)
- All cases and verdicts are hand-built toys

## Run It

```bash
cd demo-45-localisation-nulls
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_nulls.py         # writes results/nulls.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-45-localisation-nulls/INSTRUCTIONS.md).
