# Quick Start

## Prerequisites

- Python 3.11+
- Git
- Make (Linux/macOS) or run Python scripts directly (Windows)

## Installation

```bash
# Clone repository
git clone https://github.com/agentic-security-demos/agentic-security-demos.git
cd agentic-security-demos

# One-time setup (installs dependencies, generates fixtures)
make setup
```

## Running Tests

```bash
# All demos (316 tests)
make test

# Specific demo
make test DEMO=01
```

## Running Demos

```bash
# Run specific demo
make demo DEMO=01

# All demos sequentially
make all-demos
```

## Demo Output

Each demo produces:
- Console output showing attack/defense comparison
- JSON results in `demo-XX/results/` with standardized schema:

```json
{
  "demo": "demo-01-blind-verification",
  "experiment": "comparison",
  "seed": 42,
  "commit": "abc1234",
  "environment": "Python 3.11, Ubuntu 22.04",
  "command": "make demo DEMO=01",
  "result": "pass",
  "notes": "Synthetic teaching fixture"
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `make setup` |
| Tests fail with network error | Check `make verify-safety` |
| Permission denied | Ensure `make` is executable |
| Python version error | Use Python 3.11+ |

## Next Steps

- Read [Safety First](safety.md) — **Required before running demos**
- Browse [Demos Overview](demos/overview.md)
- Try [Beginner Exercises](../tutorials/beginner.md)