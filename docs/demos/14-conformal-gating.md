# Demo 14: Conformal Gating

## Learning Objectives

- Explain what a conformal risk gate is (execute an action only when its risk score is below a calibrated threshold)
- Calibrate a threshold on one episode set to meet a nominal risk budget (alpha 0.30)
- Show the guarantee holds on same-distribution episodes but breaks under benchmark shift (risk 0/1 = 0.00 vs 2/2 = 1.00)
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

Deployed agents gate every tool call: execute or block. Heuristic thresholds carry no promise. Conformal risk control picks the threshold from calibration data with a stated budget — here, at most 30% of executed actions may be injected.

This toy uses 14 hand-built episodes (6 calibration, 4 same-corpus test, 4 shifted test):

| Set | Executed (<=0.20) | Realised risk | Verdict |
|-----|-------------------|---------------|---------|
| Calibration (6) | 2/6 | 0/2 = 0.00 | threshold 0.20 chosen |
| Same-corpus (4) | 1/4 | 0/1 = 0.00 | holds (<= 0.30) |
| Shifted (4) | 2/4 | 2/2 = 1.00 | **fails** — scores mislead under shift |

Episodes `h1`/`h2` are the lesson: injected actions with low scores slip through the same gate that was safe on the calibration distribution. Coverage measures the calibration distribution more than deployment safety.

Boundary: this toy shows a calibration mechanism on fixed episodes; it is not detector tuning or cost analysis (Demo 37). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real trajectories, benchmarks, models, or credentials
- No network access (standard library only)
- All episodes, scores and verdicts are hand-built toys

## Run It

```bash
cd demo-14-conformal-gating
python3 -m pytest tests/ -v          # 6 tests, <1 min
python3 student/run_gate.py          # writes results/gating_eval.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-14-conformal-gating/INSTRUCTIONS.md).
