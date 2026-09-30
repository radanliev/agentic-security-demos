# Demo 35: Scaling Metaregression

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain why benchmark choice can dominate scale in unsafe-rate comparisons
- Compute per-benchmark means (A 0.650, B 0.345, gap 0.305) and per-scale means (small 0.464, large 0.470, gap 0.006)
- Show the benchmark gap exceeds 0.20 while the scale gap stays within 0.05
- Distinguish synthesis of published numbers from new measurements

## Conceptual Explanation

Misbehaviour is often plotted against model size, but the test suite matters
more. This toy uses ten hand-built rows: four on benchmark A (high rates) and
six on benchmark B (low rates), balanced across small (`params_B < 10`) and
large bins.

| Group | Mean unsafe rate |
|-------|------------------|
| Benchmark A (n=4) | 0.650 |
| Benchmark B (n=6) | 0.345 |
| Small scale (n=5) | 0.464 |
| Large scale (n=5) | 0.470 |

Benchmark gap 0.305 dwarfs scale gap 0.006: the suite explains more than size.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real benchmarks, models, measurements, or credentials
- No network access (standard library only)
- All rows and means are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real scaling

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 35 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=35` |

## Research Connection

This demo illustrates the synthesis question of a pending meta-analysis of
agent misbehaviour scaling targeting TMLR. That analysis has **collected no
confirmatory data**; every quantity there is `[RESULT PENDING]`. Nothing here
describes a publication, a venue result, or a measured effect size. Boundary:
this demo synthesises published-style numbers; it takes no new measurements.

Provenance: distilled from `demo-35-agent-misbehaviour-scaling-metaanalysis-tmlr` (private research repo).

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Published unsafe rates (pending) | 10 hand-built rows |
| Method | Random-effects meta-regression | Group means by benchmark and scale bin |
| Claims | Falsifiable scaling hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Meta-analysis kit | One tiny means module |
