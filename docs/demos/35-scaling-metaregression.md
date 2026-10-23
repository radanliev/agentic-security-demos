# Demo 35: Scaling Metaregression

## Learning Objectives

- Explain why benchmark choice can dominate scale in unsafe-rate comparisons
- Compute per-benchmark means (A 0.650, B 0.345, gap 0.305) and per-scale means (small 0.464, large 0.470, gap 0.006)
- Show the benchmark gap exceeds 0.20 while the scale gap stays within 0.05
- Distinguish synthesis of published numbers from new measurements

## Conceptual Explanation

Misbehaviour is often plotted against model size, but the test suite matters more. This toy uses ten hand-built rows: four on benchmark A (high rates) and six on benchmark B (low rates), balanced across small (`params_B < 10`) and large bins.

| Group | Mean unsafe rate |
|-------|------------------|
| Benchmark A (n=4) | 0.650 |
| Benchmark B (n=6) | 0.345 |
| Small scale (n=5) | 0.464 |
| Large scale (n=5) | 0.470 |

Benchmark gap 0.305 dwarfs scale gap 0.006: the suite explains more than size.

Boundary: this demo synthesises hand-built published-style rows; it is not a measurement and not model evaluation. Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real benchmarks, models, measurements, or credentials
- No network access (standard library only)
- All rows and means are hand-built toys

## Run It

```bash
cd demo-35-scaling-metaregression
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_meta.py          # writes results/meta.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-35-scaling-metaregression/INSTRUCTIONS.md).
