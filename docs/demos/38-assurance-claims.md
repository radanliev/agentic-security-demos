# Demo 38: Assurance Claims

## Learning Objectives

- Explain what coding a public claim against assurance obligations means
- Code 8 synthetic system cards against 5 obligations (threats, evals, agentic, third_party, mitigations)
- Show full coverage holds for only 2/8 cards and third-party coverage is weakest at 2/8
- Run a hand-built experiment (one flag-flip) and explain why both tallies move
- Distinguish this teaching toy from the pending longitudinal study it illustrates

## Conceptual Explanation

System cards make public claims; assurance asks whether each claim is backed by a stated obligation. Coding 8 hand-built cards against 5 obligations:

| Obligation | Covered |
|------------|---------|
| threats | 7/8 |
| evals | 5/8 |
| agentic | 4/8 |
| third_party | 2/8 (weakest) |
| mitigations | 7/8 |

Only 2/8 cards cover every obligation. The lesson: third-party evaluation is the thinnest public claim, so an assurance reader should ask for it first.

### Why flag-counting is not assurance

The demo counts boolean flags — it cannot tell a documented evaluation from an unsupported assertion. The research codebook answers this with a three-value scheme (`present` / `absent` / `vague`) plus double-coding with a reliability floor. The toy shows the arithmetic; the study must earn the interpretation.

Boundary: this demo codes assurance claims against obligations; Demo 43 codes accountability TERMS. Different sources, methods, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real system cards, vendors, or credentials
- No network access (standard library only)
- All cards, codings and verdicts are hand-built toys

## Run It

```bash
cd demo-38-assurance-claims
python3 -m pytest tests/ -v          # 19 tests, <1 min
python3 student/run_claims.py        # writes results/claims.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-38-assurance-claims/INSTRUCTIONS.md).
