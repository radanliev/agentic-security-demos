# Contributing to Agentic Security Demos

Thank you for improving these teaching materials! This project follows a standard GitHub workflow optimized for educational content.

---

## 🚀 Quick Start for Contributors

```bash
# 1. Fork → Clone → Branch
git clone https://github.com/radanliev/agentic-security-demos.git
cd agentic-security-demos
git checkout -b my-improvement

# 2. Setup (installs deps, generates fixtures)
make setup

# 3. Make your changes
# ...

# 4. Test locally (MUST pass)
make test

# 5. Safety check (MUST pass)
make verify-safety

# 6. Commit & Push
git add .
git commit -m "feat(demo-03): add saturation detection exercise"
git push origin my-improvement

# 7. Open PR on GitHub
```

---

## ✅ What We Accept

| Type | Description | Example |
|-------|-------------|---------|
| 🐛 **Bug fixes** | Fix broken tests, logic errors, typos | Fix off-by-one in demo-03 invariant |
| 📝 **Documentation** | Improve READMEs, docstrings, tutorials | Clarify provenance semantics in demo-04 |
| 🧪 **Tests** | Add missing test coverage | Add edge case for waiver expiration |
| 🎯 **Exercises** | New beginner/standard/extension exercises | Add "saturation detection" exercise |
| 🔧 **Refactoring** | Code quality (no behavior change) | Extract common test fixtures |
| 🎓 **New demos** | Following established pattern | Add demo-11 for agent memory safety |

---

## 🛡️ Safety Requirements (Non-Negotiable)

**Every PR must pass `make verify-safety`:**

| Check | What It Catches |
|-------|-----------------|
| **Zero network access** | No `import socket`, `requests`, `urllib`, `http.client`, `aiohttp`, `httpx` in test/demo code |
| **No credentials** | No `sk-`, `ghp_`, `gho_`, `ghu_`, `ghs_`, `github_pat_`, `aws_access_key`, `AWS_SECRET`, `BEGIN PRIVATE` |
| **No external URLs in tests** | Only `localhost`, `127.0.0.1`, `example.com` allowed |
| **Synthetic fixtures only** | No real IPs, hostnames, API endpoints, or datasets |
| **No executable code** | No `exec()`, `eval()`, `subprocess.run(shell=True)`, `os.system()` |

---

## 📝 Code Style

### Python (PEP 8 + Type Hints + Google Docstrings)

```python
# Good: Type hints, Google docstrings, single responsibility
def validate_target(target: Target, scope: ScopePolicy) -> tuple[bool, str]:
    """Validate target against scope policy.
    
    Args:
        target: The target to validate.
        scope: The scope policy to check against.
        
    Returns:
        Tuple of (allowed: bool, reason: str).
    """
    ...

# Bad: No types, unclear names, multiple responsibilities
def check(x, y):
    return x.check(y)
```

### Linting & Type Checking

```bash
# Auto-fix formatting & linting
ruff check . --fix --exclude demo-*/results --exclude demo-*/__pycache__ --exclude .pytest_cache --exclude .venv
ruff format . --exclude demo-*/results --exclude demo-*/__pycache__ --exclude .pytest_cache --exclude .venv

# Type checking (strict)
mypy --strict --exclude "demo-*/results,demo-*/__pycache__,.pytest_cache,.venv" \
     demo-*/student demo-*/tests shared
```

---

## 🧪 Testing

```bash
# All tests (316 tests across 10 demos + shared/)
make test

# Specific demo
make test DEMO=01

# With coverage
pytest --cov=demo-01-blind-verification/student demo-01-blind-verification/tests/

# Only exercises
pytest -k exercise
```

**Test Requirements:**
- All tests must pass
- Tests must be deterministic (seed=42)
- No network access in tests
- Tests must follow existing patterns (fixtures, parametrize, etc.)

---

## 🎯 Adding a New Demo

### 1. Create Structure
```bash
mkdir -p demo-XX-name/{fixtures,student,tests,results}
```

### 2. Required Files

| File | Required? | Description |
|------|-----------|-------------|
| `README.md` | ✅ | Learning objectives, safety notice, reproducibility |
| `fixtures/` | ✅ | Synthetic data only (JSON/YAML) |
| `student/` | ✅ | Starter code with TODO comments |
| `tests/` | ✅ | Visible correctness tests (pytest) |
| `results/` | ✅ | (gitignored, created at runtime) |
| `Makefile` | ✅ | `setup`, `test`, `demo`, `clean` |
| `solutions/` | ⚠️ | Instructor-only (excluded from public repo) |

### 2. Register in Root
- Add to root `Makefile` `DEMO_DIRS`
- Add CI test entry in `.github/workflows/ci.yml`
- Update root `README.md` demo table

### 3. Demo README Template
```markdown
# Demo XX: Name

## Learning Objectives
- Objective 1
- Objective 2

## Conceptual Explanation
...

## Safety Notice
⚠️ **Teaching demonstration using synthetic fixtures only.**
- No real [targets/credentials/network/malware]
- No network access
- All fixtures are local synthetic data

## Running
make demo DEMO=XX
```

---

## 🔍 Code Review Criteria

PRs are evaluated on:

| Criterion | Weight |
|-----------|--------|
| Educational clarity & correctness | High |
| Safety compliance (zero network, no credentials, synthetic only) | **Critical** |
| Test coverage & determinism | High |
| Reproducibility metadata completeness | High |
| Consistency with existing demos | High |
| Code quality & style | Medium |

---

## 📋 PR Checklist

- [ ] `make test` passes locally
- [ ] `make verify-safety` passes locally
- [ ] No network access added
- [ ] No real credentials or API keys
- [ ] Only synthetic fixtures used
- [ ] Safety notices in modified demo READMEs
- [ ] Standardized result schema maintained
- [ ] Tests added/updated for changes
- [ ] Documentation updated (README, docstrings)
- [ ] Beginner/standard/extension exercises included
- [ ] Reproducibility metadata (seed, commit, env, command)

---

## 🔧 Code Quality Tools

### Pre-commit Hooks (Recommended)
```bash
# Install once
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

**Configured hooks:** Ruff (lint/format), MyPy (strict), Safety check (`make verify-safety`)

---

## 🤝 Community

- **Discussions**: Questions, ideas, show-and-tell
- **Issues**: Bugs, features, docs improvements
- **Discord**: Real-time chat (placeholder)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*Thank you for contributing to safer agentic AI education!*