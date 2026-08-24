# Demo 03: Evaluation Invariants

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../../docs/course/lab-03-eval-invariants.md)

## Learning Objectives

- Design evaluations using executable invariants, not just headline scores
- Detect test leakage (train/test contamination)
- Measure task difficulty and saturation
- Verify scoring stability across runs
- Classify failure modes correctly
- Capture reproducible evaluation metadata

## Conceptual Explanation

Headline scores (e.g., "95% accuracy") are misleading without context. **Evaluation invariants** are executable checks that validate the evaluation itself:

1. **No leakage**: Test items don't appear in training data
2. **Adequate difficulty**: Tasks aren't trivially solvable
3. **Stable scoring**: Same input yields same score
4. **Correct failure classification**: Failures categorized accurately
5. **Reproducible metadata**: Seed, environment, command recorded

This demo implements a miniature evaluation suite with synthetic tasks and five invariant checks.

## Safety Notice

⚠️ **Teaching demonstration only.**
- Synthetic tasks and model outputs
- No external dataset downloads
- No model API calls
- Results are demonstrations, not research claims

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
| Command | `make demo DEMO=03` |
