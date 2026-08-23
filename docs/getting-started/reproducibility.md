# Reproducibility

## Standardized Result Schema

Every demo run produces a JSON result with these fields:

```json
{
  "demo": "demo-01-blind-verification",
  "experiment": "comparison",
  "seed": 42,
  "commit": "abc1234",
  "environment": "Python 3.11, Ubuntu 22.04",
  "command": "make demo DEMO=01",
  "result": "pass",
  "notes": "Synthetic teaching fixture",
  "timestamp": "2024-01-15T10:30:00Z",
  "duration_ms": 1234,
  "metadata": {}
}
```

## Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `demo` | Demo identifier | `demo-01-blind-verification` |
| `experiment` | Experiment name | `comparison`, `drift_detection` |
| `seed` | Random seed for determinism | `42` |
| `commit` | Git SHA or `local` | `abc1234` |
| `environment` | Python version, OS | `Python 3.11, Ubuntu 22.04` |
| `command` | Exact command run | `make demo DEMO=01` |
| `result` | `pass` \| `fail` \| `error` | `pass` |
| `notes` | Context for results | `Synthetic teaching fixture` |

## Recording Results

### For Lab Reports

Record these fields in every lab report:
1. Seed used
2. Git commit hash
3. Python version and OS
4. Exact command executed
4. Result (pass/fail)
5. Any observations

### Automated Capture

The `shared/result_schema.py` module provides:

```python
from shared.result_schema import write_result

write_result(
    demo="demo-01-blind-verification",
    experiment="my_experiment",
    seed=42,
    result="pass",
    notes="My custom experiment",
    command="make demo DEMO=01"
)
```

## Determinism

All demos use fixed seeds for reproducibility:

```python
# In shared/reproducibility.py
SEED = 42  # Global default
```

### Setting Custom Seeds

```bash
# Override seed for specific run
SEED=123 make demo DEMO=01
```

### Verifying Determinism

```bash
# Run twice with same seed - should produce identical results
make demo DEMO=01 SEED=42 > run1.json
make demo DEMO=01 SEED=42 > run2.json
diff run1.json run2.json  # Should be empty
```

## Environment Capture

The `shared/reproducibility.py` module captures:

- Python version
- Operating system and architecture
- PYTHONHASHSEED value
- Git commit hash

## Best Practices

1. **Always record seed** — Enables exact reproduction
2. **Record commit hash** — Links results to code version
3. **Note environment** — Python version matters for hash randomization
4. **Use exact commands** — Copy-paste from terminal
5. **Label as synthetic** — Never present as research results

## Example Lab Report Entry

| Field | Value |
|-------|-------|
| Demo | `demo-01-blind-verification` |
| Experiment | `blind_commitment_comparison` |
| Seed | `42` |
| Commit | `a1b2c3d4` |
| Environment | `Python 3.11.4, Ubuntu 22.04.3 LTS` |
| Command | `make demo DEMO=01 SEED=42` |
| Result | `pass` |
| Notes | `Baseline: 1/4 passed, Verified: 3/4 passed` |

---

*Remember: Teaching results are demonstrations, not validated research claims.*