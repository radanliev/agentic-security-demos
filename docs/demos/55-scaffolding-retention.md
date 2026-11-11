# Demo 55: Scaffolding Retention

## Learning Objectives

- Contrast an immediate effect against a residual effect after scaffolding stops
- Compute achieved power for a planned two-arm trial (n=40/arm, α=0.05)
- See how a shrinking effect (0.40 → 0.15) collapses power (0.43 → 0.10)
- Explain why an underpowered retention test cannot "confirm" persistence
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A synthetic two-arm trial measures learning with and without a scaffold. The
catch: the effect shrinks once the scaffold is removed.

| Contrast | Difference | Achieved power |
|----------|-----------|----------------|
| immediate (with scaffold) | 0.40 | 0.432 |
| residual (scaffold removed) | 0.15 | 0.103 |

At n=40 per arm the immediate contrast is already underpowered; the residual
contrast is close to the 10% floor — a non-significant residual result is
uninformative, not evidence of decay. The design, not the statistic, decides
what the trial can see.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real participants, interventions, or outcomes
- No network access (standard library only)
- All numbers are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real trials

## Run It

```bash
cd demo-55-scaffolding-retention
python3 -m pytest tests/ -v          # 3 tests, <1 min
python3 student/run_power.py         # writes results/power.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-55-scaffolding-retention/INSTRUCTIONS.md).
