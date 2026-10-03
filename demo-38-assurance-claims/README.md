# Demo 38: Assurance Claims

<p align="center">
  <img src="https://img.shields.io/badge/Teaching%20demo-Synthetic%20only-blue?style=flat-square" alt="Teaching demo">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Network-Offline%20only-success?style=flat-square" alt="Offline only">
</p>

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants.

## Learning Objectives

- Explain what coding a public claim against assurance obligations means
- Code 8 synthetic system cards against 5 obligations (threats, evals, agentic, third_party, mitigations)
- Show full coverage holds for only 2/8 cards and third-party coverage is weakest at 2/8
- Run a hand-built experiment (one flag-flip) and explain why both tallies move
- Distinguish this teaching toy from the pending FAccT 2027 longitudinal study it illustrates

## Conceptual Explanation

System cards make public claims; assurance asks whether each claim is backed
by a stated obligation. Coding 8 hand-built cards against 5 obligations:

| Obligation | Covered |
|------------|---------|
| threats | 7/8 |
| evals | 5/8 |
| agentic | 4/8 |
| third_party | 2/8 (weakest) |
| mitigations | 7/8 |

Only 2/8 cards cover every obligation. The lesson: third-party evaluation is
the thinnest public claim, so an assurance reader should ask for it first.

### Why flag-counting is not assurance

The demo counts boolean flags — it cannot tell a documented evaluation from an
unsupported assertion. The research codebook answers this with a three-value
scheme (`present` / `absent` / `vague`) plus double-coding with a reliability
floor. The toy shows the arithmetic; the study must earn the interpretation.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real system cards, vendors, or credentials
- No network access (standard library only)
- All cards, codings and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real cards
- Responsible-use rules: [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md)

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 38 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Tests | `python3 -m pytest tests/ -v` → 19 passed |
| Command | `make demo DEMO=38` (from repo root) or `make demo` (from this directory) |
| Result file | `results/claims.json` |

## Research Connection

This demo illustrates the design question of a longitudinal study of system
card assurance claims (targeting ACM FAccT 2027, Plan A). That study is
**pending**; every quantity there is `[RESULT PENDING]` and its registration
thresholds are undecided (`AD-90` in the paper repository). Nothing here
describes a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-38-system-card-assurance-claims-joc` (private research repo).
It shares no topic with Demo 39 (incident taxonomy): this demo codes public
CLAIMS against obligations; Demo 39 codes incident reports into patterns.
Different sources, methods, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Longitudinal corpus of real system cards (pending) | 8 hand-built cards |
| Method | Coded content analysis over time, double-coded with reliability floor | Single fixed coding table |
| Obligations | AI Act, GPAI Code, NIST RMF mapped per codebook | 5 toy labels |
| Claims | Falsifiable coverage-trend hypotheses (registered) | **No claims** — mechanism illustration only |
| Artefact | Coding protocol with reliability checks | One tiny coverage function |

### Difference from the Benchmark (there is none — and that is the point)

Unlike demos that wrap a published benchmark, this demo has no external
benchmark to beat: the "expected" table in INSTRUCTIONS.md Step 4 is the
fixture's own arithmetic, pinned by 19 tests. A changed table with passing
tests would mean the fixture changed, not that assurance improved. The
research study earns external validity through real cards, double-coding, and
registration — none of which this toy has.
