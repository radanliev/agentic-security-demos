# Demo 53: Human Validation

## Learning Objectives

- Plant known errors in a known proportion before validating
- Draw a fixed sample and compute planted-error coverage
- Distinguish item error rate from sample error rate
- Explain why sampling without planted ground truth cannot measure quality
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Eight synthetic agent outputs, three with planted errors. A reviewer checks a
sample of four and finds every planted error in the sample.

| Quantity | Value |
|----------|-------|
| Items / planted errors | 8 / 3 |
| Sample | a2, a4, a5, a8 |
| Planted errors in sample | 3/3 (coverage 1.0) |
| Sample error rate | 0.75 |

The planted errors are the measuring stick: without them "I reviewed some
outputs" is an anecdote, not a validation.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real annotators, workers, or outputs
- No network access (standard library only)
- All items are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real pipelines

## Run It

```bash
cd demo-53-human-validation
python3 -m pytest tests/ -v          # 3 tests, <1 min
python3 student/run_validate.py      # writes results/validation.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-53-human-validation/INSTRUCTIONS.md).
