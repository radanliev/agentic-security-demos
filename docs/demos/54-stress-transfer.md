# Demo 54: Stress Transfer

## Learning Objectives

- Build an in-distribution stress suite and a shifted twin
- Measure recall collapse under distribution shift
- Explain why a perfect detector in-distribution proves little
- Read the gap metric: recall drop and accuracy drop
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

One detector, threshold 0.5, two suites of four items. In-distribution it is
perfect; under shift it misses every attack.

| Suite | Recall | FPR | Accuracy | Missed attacks |
|-------|--------|-----|----------|----------------|
| in_distribution | 1.00 | 0.00 | 1.00 | 0 |
| shifted | 0.00 | 0.00 | 0.50 | 2 |

Gap: recall drop 1.0, accuracy drop 0.5. The shifted suite keeps the same
attack types but changes the surface features — exactly the kind of change a
benchmark-trained detector never saw. Passing the stress test did not
transfer.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real attacks, detectors, or deployments
- No network access (standard library only)
- Both suites are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real detectors

## Run It

```bash
cd demo-54-stress-test-transfer
python3 -m pytest tests/ -v          # 3 tests, <1 min
python3 student/run_transfer.py      # writes results/transfer.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-54-stress-test-transfer/INSTRUCTIONS.md).

## Relationship to Demos 37 and 51

Demo 37 prices detector errors; demo 51 asks who bears false positives; this
demo asks whether the measured error rates survive a shifted world.
