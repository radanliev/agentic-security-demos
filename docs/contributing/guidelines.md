# Contributing Guidelines

## Overview

We welcome contributions to Agentic Security Demos! This guide covers everything you need to know.

## Quick Start

```bash
# Fork → Clone → Branch
git clone https://github.com/your-fork/agentic-security-demos.git
cd agentic-security-demos
git checkout -b my-improvement

# Setup
make setup

# Make changes
# ...

# Test
make test
make verify-safety

# Commit & Push
git add .
git commit -m "Improve demo-03: add saturation detection"
git push origin my-improvement

# Open PR on GitHub
```

## What We Accept

| Type | Description |
|-------|-------------|
| 🐛 Bug fixes | Fix broken tests, logic errors, typos |
| 📝 Documentation | Improve READMEs, docstrings, tutorials |
| 🧪 Tests | Add missing test coverage |
| 🎯 Exercises | New beginner/standard/extension exercises |
| 🔧 Refactoring | Code quality improvements (no behavior change) |
| 🎓 New demos | Following established pattern |
| 🛡️ Safety | New safety checks or improvements |

## What We Don't Accept

- Network access in tests/demos
- Real credentials, API keys, or private keys
- Executable malware or exploit code
- Real network targets or scanning
- Research claims presented as validated results

## Code Style

### Python

- **PEP 8** with **type hints** (mypy strict)
- **Google-style docstrings** for public APIs
- **Small functions** — single responsibility
- **No global state** — prefer dependency injection

```python
# Good
def validate_scope(scope: ScopePolicy, target: Target) -> tuple[bool, str]:
    """Validate target against scope policy.
    
    Args:
        scope: The scope policy to check against.
        target: The target to validate.
        
    Returns:
        Tuple of (allowed: bool, reason: str).
    """
    ...

# Bad
def check(x, y):  # No types, unclear names
    return x.check(y)
```

### Linting

```bash
# Auto-fix
ruff check . --fix
ruff format .

# Check only
ruff check .
ruff format --check .
```

### Type Checking

```bash
mypy --strict --exclude "demo-*/results,demo-*/__pycache__,.pytest_cache,.venv" \
     demo-*/student demo-*/tests shared
```

## Testing

```bash
# All tests
make test

# Specific demo
make test DEMO=01

# With coverage
pytest --cov=demo-01-blind-verification/student demo-01-blind-verification/tests/

# Only exercises
pytest -k exercise
```

## Safety Requirements

**Every PR must pass `make verify-safety`:**

- ✅ Zero network imports in test/demo code
- ✅ No credentials (sk-, ghp_, AWS_SECRET, etc.)
- ✅ No external URLs in tests (localhost/example.com allowed)
- ✅ Synthetic fixtures only
- ✅ Standardized result schema

## Adding a New Demo

### 1. Create Structure

```bash
mkdir -p demo-XX-name/{fixtures,student,tests,results}
```

### 2. Required Files

| File | Required? |
|------|-----------|
| `README.md` | ✅ Learning objectives, safety notice, reproducibility |
| `fixtures/` | ✅ Synthetic data only |
| `student/` | ✅ Starter code with TODOs |
| `tests/` | ✅ Beginner/standard/extension exercises |
| `results/` | ✅ (gitignored, created at runtime) |
| `Makefile` | ✅ setup, test, demo, clean |
| `pyproject.toml` | Optional (demo-specific deps) |

### 3. Register in Root

- Add to root `Makefile` DEMO_DIRS
- Add CI test entry in `.github/workflows/ci.yml`
- Update root `README.md` demo table

### 4. Demo README Template

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

## PR Checklist

- [ ] `make test` passes
- [ ] `make verify-safety` passes
- [ ] No network access added
- ✅ No credentials added
- ✅ Synthetic fixtures only
- ✅ Safety notices in README
- ✅ Tests for new functionality
- ✅ Documentation updated
- ✅ Exercises at all levels
- ✅ Reproducibility metadata (seed, commit, env, command)

## Review Process

1. **Automated checks** — CI runs all tests, safety, quality
2. **Maintainer review** — Code review by demo owner
3. **Safety review** — Security team checks safety guarantees
4. **Merge** — Squash merge to main

## Community

- **Discussions** — Questions, ideas, show-and-tell
- **Issues** — Bugs, features, docs improvements
- **Discord** — Real-time chat (placeholder)

---

*Thank you for contributing to safer agentic AI education!*