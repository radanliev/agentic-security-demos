# Installation

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.11 | 3.11+ |
| OS | Linux/macOS/Windows | Linux/macOS |
| RAM | 512 MB | 1 GB |
| Disk | 100 MB | 500 MB |

## Dependencies

### Core (installed via `make setup`)
- `pytest>=7.4.0` — Testing framework
- `pyyaml>=6.0` — YAML parsing
- `cryptography>=41.0.0` — Cryptographic primitives

### Development (optional)
```bash
pip install -e .[dev]
# Installs: pytest-cov, mypy, ruff, pre-commit
```

## Platform-Specific Notes

### Linux/macOS
```bash
# Standard installation works
make setup
```

### Windows
```powershell
# Use PowerShell or WSL
python -m pip install -r requirements.txt
python -m pytest demo-01-blind-verification/tests/
# Run demos directly:
python demo-01-blind-verification/student/baseline_agent.py
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["make", "test"]
```

## Verifying Installation

```bash
# Run all tests
make test

# Expected output: "=== All tests passed ==="
# 170 tests across 10 demos

# Quick safety check
make verify-safety
# Should output: "=== Safety verification passed ==="
```

## Updating

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
make setup

# Run tests to verify
make test
```

## Uninstalling

```bash
# Remove generated files
make clean

# Remove virtual environment (if used)
rm -rf .venv

# Remove repository
cd .. && rm -rf agentic-security-demos
```