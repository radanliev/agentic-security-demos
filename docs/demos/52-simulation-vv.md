# Demo 52: Simulation V&V

## Learning Objectives

- Separate an honest simulator from a memoriser using held-out modules
- Read held-out error (MAE) as a generalisation check
- Use a contamination probe: relabel a module and watch the prediction
- Explain why a memoriser cannot answer questions it never memorised
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Two synthetic "cohort simulators" predict module pass rates. The honest one
learned a mapping; the memoriser stored the answers.

| Check | Honest | Memoriser |
|-------|--------|-----------|
| held-out pass MAE | 0.0625 | 0.250 |
| held-out withdraw MAE | 0.055 | 0.155 |
| probe (module AAA presented as "ZZZ") | 0.62 — transfers | 0.00 — fails to transfer |

The probe is the tell: rename a known module and the honest simulator still
predicts ~0.62 (the features transfer); the memoriser answers 0.00 because it
never memorised the fake name. Validation needs both held-out error and a
contamination probe.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real students, cohorts, or institutional data
- No network access (standard library only)
- Both simulators are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real simulators

## Run It

```bash
cd demo-52-llm-sim-validation
python3 -m pytest tests/ -v          # 3 tests, <1 min
python3 student/run_sim.py           # writes results/sim_validation.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-52-llm-sim-validation/INSTRUCTIONS.md).

## Relationship to Demos 53 and 55

Demo 53 validates agent outputs by sampled human review; demo 55 checks the
analytic power of a two-arm contrast. Together with this demo they cover the
validation stack: simulator, outputs, and design.
