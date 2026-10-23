# Demo 46: Embedding Drift

## Learning Objectives

- Compute cosine shift `1 - cosine(baseline, replacement)` for one artefact
- Compare a toy swap with a frozen study mean (0.1222)
- See that an orthogonal swap moves farther than that frozen mean

## Conceptual Explanation

Supply-chain artefacts are embedded, and swapping the embedding model silently changes the similarity space. This toy computes the cosine shift between a baseline vector and a replacement on two hand-built 4-dimensional vector pairs: a small swap (shift 0.0202, below the frozen mean) and an orthogonal swap (shift 1.0000, above it).

| Swap | Shift | Above frozen mean 0.1222? |
|------|-------|---------------------------|
| small | 0.0202 | no |
| orthogonal | 1.0000 | yes |

The lesson: an orthogonal replacement moves farther than the frozen study mean — the drift number depends entirely on how far apart the representations are.

Boundary: this toy teaches the shift formula on two hand-built vectors; the frozen mean is a label copied from the simulated study for comparison, not a new measurement. No models, no network, no package corpus.

## Safety Notice

⚠️ **Teaching demonstration only.**
- Synthetic 4-dimensional vectors only
- No real models, packages, registries, or credentials
- No network access (standard library only)

## Run It

```bash
cd demo-46-embedding-drift
python3 -m pytest tests/ -v          # 4 tests, <1 min
python3 student/run_drift.py         # writes results/drift.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-46-embedding-drift/INSTRUCTIONS.md).
