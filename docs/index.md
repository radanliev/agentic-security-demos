# Documentation Index

## Demo Guides

Each demo has its own README.md with:
- Learning objectives
- Conceptual explanation
- Safety notice
- Reproducibility metadata
- Difference from private research

## Running Demos

```bash
# Run all tests
make test

# Run specific demo
make demo DEMO=01

# Run demo with custom experiment
make demo DEMO=03 EXPERIMENT=leakage
```

## Result Schema

All demos produce standardized JSON results:

```json
{
  "demo": "demo-XX-name",
  "experiment": "experiment-name",
  "seed": 42,
  "commit": "git-sha-or-local",
  "environment": "Python 3.11, Ubuntu 22.04",
  "command": "make demo DEMO=XX",
  "result": "pass|fail",
  "notes": "Synthetic teaching fixture"
}
```

## Safety Requirements

See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md) and [SECURITY.md](../SECURITY.md).

## Extending Demos

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding exercises or new demos.