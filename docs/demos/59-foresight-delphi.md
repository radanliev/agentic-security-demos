# Demo 59: Foresight Delphi

## Learning Objectives

- Run a two-round synthetic Delphi with five panelists
- Summarise ratings with median, quartiles, and IQR
- Declare consensus ex ante (IQR threshold) and apply it mechanically
- Bind every summary to a briefing hash so ratings have an anchor
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Two synthetic policy questions, five panelists each, one briefing hash.

| Question | Median | IQR | Consensus |
|----------|--------|-----|-----------|
| P1 | 6.0 | 1.5 | yes |
| P2 | 3.0 | 3.0 | no |

P1's tight spread meets the pre-declared IQR rule; P2's wide spread does not,
so P2 carries no consensus claim — the rule, not the facilitator, decides.
The briefing hash makes "consensus about what" checkable after the fact.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real experts, panels, or forecasts
- No network access (standard library only)
- All ratings are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real foresight

## Run It

```bash
cd demo-59-foresight-delphi
python3 -m pytest tests/ -v          # 3 tests, <1 min
python3 student/run_delphi.py        # writes results/delphi.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-59-foresight-delphi/INSTRUCTIONS.md).
