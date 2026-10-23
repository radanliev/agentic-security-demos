# Demo 37: Detector Cost

## Learning Objectives

- Explain why detector choice is an operating-point decision, not an accuracy contest
- Score a strict substring detector and a lenient exact-phrase detector on the same 10 synthetic prompts
- Price false positives at 10 and false negatives at 25, and show the strict detector wins on cost (20 vs 50)
- Distinguish this teaching toy from the pending practitioner evaluation it illustrates

## Conceptual Explanation

A detector that catches everything also cries wolf. On these 10 hand-built prompts (4 injected, 6 benign), the strict rule (`ignor*` substring) catches 4/4 injections but false-alarms on 2/6 benign prompts, including two tricky ones: a request to "ignore the previous email thread" (benign context) and a mention of "the ignore button". The lenient rule (exact phrase "ignore previous instructions") misses the 2 paraphrased injections but never false-alarms.

| Detector | TP | FP | FN | Cost (FP=10, FN=25) |
|----------|----|----|----|----------------------|
| Strict | 4/4 | 2/6 | 0/4 | 2×10 + 0×25 = 20 |
| Lenient | 2/4 | 0/6 | 2/4 | 0×10 + 2×25 = 50 |

Lesson: under asymmetric costs, the noisier detector is the cheaper one. Tune the threshold with costs, not accuracy.

Boundary: this demo prices fixed detectors on text prompts; it is not the visual channel (Demo 34). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real prompts, models, detectors, or credentials
- No network access (standard library only)
- All prompts, flags and costs are hand-built toys

## Run It

```bash
cd demo-37-detector-cost
python3 -m pytest tests/ -v          # 21 tests, <1 min
python3 student/run_cost.py          # writes results/detector_cost.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-37-detector-cost/INSTRUCTIONS.md).
