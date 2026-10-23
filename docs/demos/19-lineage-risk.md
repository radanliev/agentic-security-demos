# Demo 19: Lineage Risk

## Learning Objectives

- Explain inherited supply-chain risk (a clean child of a flagged parent is still risky)
- Classify 8 synthetic models by own flags vs inherited risk
- Show 6/8 risky: 1 origin, 2 introduced, 3 inherited
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

Models derive from parents: fine-tunes, merges, re-uploads. A pickled parent, a remote-code parent, or a licence problem flows downhill even when the child looks clean. This toy uses 8 hand-built models: 6/8 risky (1 origin, 2 introduced, 3 inherited).

Boundary: this demo is weight-supply-chain inheritance; it is not model-card disclosure analysis (Demo 36). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real model hub data, weights, models, or credentials
- No network access (standard library only)
- All models, flags and verdicts are hand-built toys

## Run It

```bash
cd demo-19-lineage-risk
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_lineage.py       # writes results/lineage.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-19-lineage-risk/INSTRUCTIONS.md).
