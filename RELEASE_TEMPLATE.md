# Release Note Template

Use this template when creating a new release (tag `vX.Y.Z`).

---

## Release Notes Template: `vX.Y.Z`

### 🎯 Highlights
- **Major**: Brief description of major changes
- **Minor**: New demos, features, exercises
- **Patch**: Bug fixes, doc improvements, safety fixes

---

### 🚀 New Demos / Major Features
- `demo-XX-name`: Brief description of what it teaches
  - Learning objectives: ...
  - Key concepts: ...

---

### ✨ Enhancements
- **Demo XX**: Specific improvement (e.g., "Added saturation detection invariant to demo-03")
- **Demo XX**: New exercise level (e.g., "Added extension exercise for provenance chaining")

---

### 🐛 Bug Fixes
- **Demo XX**: Fixed issue where... (link to issue #XXX)
- **Root**: Fixed CI flakiness in...

---

### 📚 Documentation
- Updated README with...
- Added tutorial for...
- Clarified safety notice in demo-XX...

---

### 🛡️ Safety & Security
- Added safety check for...
- Updated credential scanning patterns...
- Fixed potential path traversal in...

---

### 🔬 Reproducibility
- Updated seed handling for...
- Improved environment capture...

---

### 📦 Dependency Updates
- Updated `cryptography` from X.Y.Z to A.B.C
- Pinned GitHub Actions to specific SHAs

---

### 👥 Contributors
Thanks to @username1, @username2 for their contributions!

---

### 🔗 Links
- [Full Changelog](CHANGELOG.md)
- [Documentation](https://radanliev.github.io/agentic-security-demos/)
- [Security Policy](SECURITY.md)

---

## How to Use This Template

1. **Copy this template** when drafting a release
2. **Fill in sections** relevant to the release
3. **Remove empty sections** (don't leave empty headers)
4. **Link related issues/PRs** using `#123` syntax
4. **Tag the release**: `git tag -a vX.Y.Z -m "Release vX.Y.Z"` then `git push origin vX.Y.Z`
5. **GitHub Actions** will auto-build docs and run full test suite

---

## Version Numbering (SemVer)

| Type | When | Example |
|------|------|---------|
| **Major** | Breaking changes, demo removal, API changes | `1.0.0` → `2.0.0` |
| **Minor** | New demo, new exercise level, new feature | `1.0.0` → `1.1.0` |
| **Patch** | Bug fix, doc update, safety fix | `1.0.0` → `1.0.1` |

---

## Pre-Release Checklist

- [ ] `make test` passes (all 316 tests; 315 passed + 1 expected failure)
- [ ] `make verify-safety` passes
- [ ] `make clean && make test` passes (clean build)
- [ ] `CHANGELOG.md` updated
- [ ] `CITATION.cff` version updated
- [ ] `pyproject.toml` version updated
- [ ] Documentation builds: `cd docs && mkdocs build`
- [ ] Security scan: `make verify-safety`
- [ ] All demos run: `make all-demos`

---

*Template version: 1.0 | Last updated: 2024-08-23*