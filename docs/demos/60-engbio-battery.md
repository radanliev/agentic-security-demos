# Demo 60: EngBio Battery

## Learning Objectives

- Score an agent against three predeclared synthetic engineering-biology tasks
- Compare predictions to frozen reference answers before any reveal
- Treat the battery as one accuracy number over heterogeneous task kinds
- Explain why predeclared references prevent post-hoc grading drift
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

A synthetic analysis battery: count an HPLC peak set, classify a growth curve,
verify a construct's part list. Three tasks, three reference answers frozen
before the agent runs.

| Task | Kind | Predicted | Reference | Correct |
|------|------|-----------|-----------|---------|
| hplc-peak | peak count | 2 | 2 | ✓ |
| growth-shape | growth | flat | flat | ✓ |
| construct-parts | construct | true | true | ✓ |

Accuracy 3/3 = 1.0 on toys. The interesting property is procedural: because
the references were declared first, a wrong answer could not have been graded
right.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real laboratory data, protocols, or organisms
- No network access (standard library only)
- All tasks and references are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real agents

## Run It

```bash
cd demo-60-engbio-battery
python3 -m pytest tests/ -v          # 4 tests, <1 min
python3 student/run_battery.py       # writes results/battery.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-60-engbio-battery/INSTRUCTIONS.md).

## Relationship to Demo 47

Demo 47 seals an answer before the key opens; this demo freezes the key
before the agent answers — pre-registration from the grader's side.
