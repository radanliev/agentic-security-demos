# Safety Checklist for Contributors

## Before Submitting PR

Run these checks locally:

```bash
# 1. All tests pass
make test

# 2. Safety verification passes
make verify-safety

# 3. Code quality passes
ruff check . --exclude demo-*/results --exclude demo-*/__pycache__ --exclude .pytest_cache --exclude .venv
mypy --strict --exclude "demo-*/results,demo-*/__pycache__,.pytest_cache,.venv" demo-*/student demo-*/tests shared
```

## Safety Requirements Checklist

### Network Access

- [ ] No `import socket`, `requests`, `urllib`, `http.client`, `aiohttp`, `httpx` in test/demo code
- [ ] No `subprocess.run` with network commands
- [ ] No external API calls
- [ ] All fixtures are local files

### Credentials

- [ ] No `sk-`, `ghp_`, `gho_`, `ghu_`, `ghs_`, `github_pat_` prefixes
- [ ] No `aws_access_key`, `AWS_SECRET`, `private_key`
- [ ] No `BEGIN PRIVATE KEY`, `-----BEGIN` patterns
- [ ] Demo keys only: `DEMO_KEY_*` generated at runtime

### Fixtures

- [ ] All JSON/YAML fixtures are synthetic
- [ ] No real IPs (use 192.168.x.x, 10.x.x.x, 127.0.0.1)
- [ ] No real hostnames (use localhost, scan-target.local)
- [ ] No real API endpoints
- [ ] Seed field present for reproducibility

### Code Patterns

- [ ] No `exec()`, `eval()`, `subprocess.run()` with shell=True
- [ ] No `os.system()`, `os.popen()`
- [ ] No `__import__()` dynamic imports
- [ ] No dynamic code generation

### Results

- [ ] All results follow standardized schema
- [ ] `notes` field includes "Synthetic teaching fixture"
- [ ] Seed, commit, environment, command recorded

## Common Violations

| Violation | Example | Fix |
|-----------|---------|-----|
| Network import | `import requests` | Use local fixtures |
| Real IP | `"8.8.8.8"` | Use `"192.168.1.1"` |
| Real hostname | `"api.github.com"` | Use `"localhost"` |
| API key | `"sk-abc123"` | Use `"DEMO_KEY_abc123"` |
| External URL | `"https://api.example.com"` | Use `"http://localhost:8080"` |
| Subprocess shell | `subprocess.run("ls", shell=True)` | Use `subprocess.run(["ls"])` |

## Verifying Safety

```bash
# Run all safety checks
make verify-safety

# Manual checks
grep -r "import requests" demo-*/tests/
grep -r "sk-" demo-*/ --include="*.py" --include="*.json"
grep -r "http://" demo-*/tests/ | grep -v "localhost\|127.0.0.1"
```

## CI Safety Gates

The CI pipeline will **fail** if:

1. Network imports found in test/demo code
2. Credential patterns detected
3. External URLs in tests (non-localhost)
4. Result schema inconsistent

## Questions?

- Check [SECURITY.md](../SECURITY.md) for vulnerability reporting
- Open a [Discussion](https://github.com/agentic-security-demos/agentic-security-demos/discussions) for clarification
- Tag `@security-owner` in PR for safety review