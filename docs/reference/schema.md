# Result Schema Reference

## Standardized Result Format

Every demo produces JSON results with this schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["demo", "experiment", "seed", "commit", "environment", "command", "result", "notes"],
  "properties": {
    "demo": {"type": "string", "pattern": "^demo-\\d{2}-[a-z-]+$"},
    "experiment": {"type": "string"},
    "seed": {"type": "integer", "minimum": 0},
    "commit": {"type": "string"},
    "environment": {"type": "string"},
    "command": {"type": "string"},
    "result": {"type": "string", "enum": ["pass", "fail", "error"]},
    "notes": {"type": "string"},
    "timestamp": {"type": "string", "format": "date-time"},
    "duration_ms": {"type": "integer", "minimum": 0},
    "metadata": {"type": "object"}
  }
}
```

## Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `demo` | string | ✅ | Demo identifier (e.g., `demo-01-blind-verification`) |
| `experiment` | string | ✅ | Experiment name (e.g., `comparison`, `drift_detection`) |
| `seed` | integer | ✅ | Random seed for determinism (default: 42) |
| `commit` | string | ✅ | Git SHA or `local` |
| `environment` | string | ✅ | Python version, OS (e.g., `Python 3.11, Ubuntu 22.04`) |
| `command` | string | ✅ | Exact command run (e.g., `make demo DEMO=01`) |
| `result` | string | ✅ | `pass`, `fail`, or `error` |
| `notes` | string | ✅ | Context (always includes `Synthetic teaching fixture`) |
| `timestamp` | string | Optional | ISO 8601 UTC timestamp |
| `duration_ms` | integer | Optional | Execution time in milliseconds |
| `metadata` | object | Optional | Demo-specific additional data |

## Example Results

Values below are from a real run of the patched repository (`make all-demos` at commit `71b37fc`); `commit`, `environment` and `result` are computed by every generator, never typed in.

### Demo 01: Comparison Table

```json
{
  "demo": "demo-01-blind-verification",
  "experiment": "comparison",
  "seed": 42,
  "commit": "71b37fc",
  "environment": "Python 3.11.15, Linux",
  "command": "make demo DEMO=01",
  "result": "pass",
  "notes": "Synthetic teaching fixture",
  "comparison": {
    "baseline": {"method": "post_hoc_with_oracle_access", "hash_bound": false, "passed": 4, "total": 4},
    "verified": {"method": "blind_commitment", "hash_bound": true, "passed": 3, "total": 4}
  }
}
```

### Demo 02: Drift Detection

```json
{
  "demo": "demo-02-supply-chain-aibom",
  "experiment": "drift_detection",
  "seed": 42,
  "commit": "71b37fc",
  "environment": "Python 3.11.15, Linux",
  "command": "make demo DEMO=02",
  "result": "pass",
  "notes": "Synthetic teaching fixture; evaluated at fixture evaluation_time 2025-01-14T12:00:00Z",
  "scenarios": [
    {"scenario": "compliant-001", "expected": "pass", "compliant": true, "drift_detected": false, "waiver_accepted": null, "matches_expected": true},
    {"scenario": "drifted-002", "expected": "block", "compliant": false, "drift_detected": true, "waiver_accepted": null, "matches_expected": true}
  ]
}
```

### Demo 05: Benchmark

```json
{
  "demo": "demo-05-eviassure",
  "experiment": "benchmark",
  "seed": 42,
  "commit": "71b37fc",
  "environment": "Python 3.11.15, Linux 6.18.44-fc-v21",
  "command": "make demo DEMO=05",
  "result": "pass",
  "notes": "Synthetic teaching fixture; min of 5 runs; timings are machine-dependent, verdicts are not",
  "benchmarks": [
    {"trace_size": 10, "chain_build_ms": 0.07, "verify_time_ms": 0.07, "proof_length": 4},
    {"trace_size": 50, "chain_build_ms": 0.36, "verify_time_ms": 0.47, "proof_length": 6}
  ]
}
```

## Usage in Lab Reports

Record these fields for every experiment:

| Field | Your Value |
|-------|------------|
| demo | |
| experiment | |
| seed | |
| commit | |
| environment | |
| command | |
| result | |
| notes | |

## Validation

```bash
# Validate result file against schema
python -c "
import json, sys
schema_keys = {'demo','experiment','seed','commit','environment','command','result','notes'}
with open('results/file.json') as f:
    data = json.load(f)
missing = schema_keys - set(data.keys())
if missing:
    print(f'Missing keys: {missing}')
    sys.exit(1)
print('Valid!')
"
```

## Notes

- **All fields are required** for reproducibility
- **Seed must be recorded** for exact reproduction
- **Commit hash** links results to code version
- **Notes must include** `Synthetic teaching fixture`
- **Results are demonstrations**, not validated research claims