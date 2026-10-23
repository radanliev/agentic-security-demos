# Demo 15: Hijack Probes

## Learning Objectives

- Explain what a white-box hijack probe is (flag an episode when its probe score meets a fixed threshold)
- Apply a fixed threshold (0.55) to 8 synthetic episodes and read the outcome table
- Show the probe catches 3/4 hijacked episodes with 0/4 false positives, missing borderline `h4`
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

Deployed monitors score each episode for hijack signatures and flag the suspicious ones. A fixed threshold trades catches against false alarms.

This toy uses 8 hand-built episodes (4 clean, 4 hijacked). Clean episodes score 0.10–0.50; hijacked episodes 0.60, 0.75, 0.90 — and `h4` at 0.45:

| Episode | Score | Truth | Flagged (>= 0.55) |
|---------|-------|-------|-------------------|
| c1–c4 | 0.10–0.50 | clean | no |
| h1–h3 | 0.60–0.90 | hijacked | yes |
| h4 | 0.45 | hijacked | **no (missed)** |

Episode `h4` is the lesson: a borderline hijacked episode below threshold slips through the same probe that catches the obvious cases.

Boundary: this toy reads a score column against a fixed threshold; it is not detector tuning or cost analysis (Demo 37). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real trajectories, probes, models, or credentials
- No network access (standard library only)
- All episodes, scores and verdicts are hand-built toys

## Run It

```bash
cd demo-15-hijack-probes
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_probe.py         # writes results/probe_eval.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-15-hijack-probes/INSTRUCTIONS.md).
