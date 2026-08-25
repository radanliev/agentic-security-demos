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

## Conference Paper Alignment (Paper 3: NeurIPS)

This demo is the educational companion to **Conference Paper 3** (`demo-3-eval-design-invariants-neurips`):
> **Evaluation Invariants for Autonomous AI Agents: Auditing Leakage, Saturation, and Validity Beyond Headline Scores** (NeurIPS)

### The 5 Executable Invariants

| # | Evaluation Invariant | Failure Mode Caught | Benchmark Risk Prevented |
|---|---|---|---|
| **1** | **No Test Leakage** | N-gram / semantic overlap between train & test | Memorization masquerading as reasoning |
| **2** | **Adequate Difficulty** | Low variance / score saturation ($100\%$ ceiling) | Construct invalidity / trivial benchmark |
| **3** | **Scoring Stability** | High score variance across deterministic re-evals | Non-deterministic / flaking evaluation harness |
| **4** | **Failure Classification** | Unclassified / misattributed agent failure modes | Erroneous safety / performance attribution |
| **5** | **Reproducible Metadata** | Missing seeds, software versions, command strings | Irreproducible empirical evaluation |

### Key Takeaway: The Four-Arm Evaluation Table

A headline score of **88%** on a benchmark with **0 invariants passed** is worthless because leakage and triviality inflate the score. A score of **81%** on an evaluation harness with **5/5 invariants passed** represents true, falsifiable capability.

## Difference from Private Research Benchmark

| Aspect | Research Benchmark (Paper 3) | This Teaching Demo (Demo 03) |
|--------|------------------------------|-----------------------------|
| Scale | 500+ multi-step agent trajectories | Synthetic 5-task evaluation fixture |
| Invariant 1 | Token-level minhash + semantic embeddings | 3-gram string overlap check |
| Invariant 2 | Item Response Theory (IRT) difficulty curves | Empirical mean & variance checks |
| Invariant 3 | Bootstrapped confidence interval stability | Deterministic re-run verification |
