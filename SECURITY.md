# Security Policy

## 🔒 Reporting Security Vulnerabilities

**Do NOT open a public issue for security vulnerabilities.**

If you discover a security issue in these teaching materials or the underlying patterns they teach:

1. **Email privately**: `security@agentic-security-demos.example` (replace with actual contact)
2. **Include**: Steps to reproduce, potential impact, affected demos/modules
3. **Allow time**: Allow 7 days for assessment before any coordinated disclosure

We take all security reports seriously and will acknowledge receipt within 48 hours.

---

## 🛡️ Scope of This Policy

### ✅ Covered
- Teaching repository code and test suites
- Synthetic fixtures and generated demo keys (explicitly non-production)
- Student exercise solutions and starter code
- CI/CD workflows and GitHub Actions
- Documentation and example code

### ❌ Not Covered
- Private research repositories that inspired these demos
- External systems students might incorrectly target
- Production deployments of patterns taught here
- Third-party dependencies (report to their maintainers)

---

## 🛡️ Safety by Design (Built-in Protections)

These demos are engineered with **defense-in-depth** safety guarantees:

| Layer | Protection | Verification |
|-------|------------|--------------|
| **Network** | Zero I/O in tests/demos | `make verify-safety` scans imports |
| **Credentials** | No persistent secrets | Regex scan for key patterns |
| **Execution** | No executable payloads | Static analysis + review |
| **Data** | Synthetic fixtures only | Content scanning |
| **Defaults** | Fail-closed policy gates | Tested in each demo |

### Verification Commands

```bash
# Run all safety checks locally
make verify-safety

# Checks performed:
# 1. No network imports (socket, requests, urllib, http.client, aiohttp, httpx)
# 2. No credential patterns (sk-, ghp_, ghp_, github_pat_, AWS_SECRET, etc.)
# 3. No external URLs in tests (allows localhost, 127.0.0.1, example.com)
# 2. Result schema consistency across all demos
```

---

## 🚨 Vulnerability Classes We Monitor

Given this is a **security education** repository, we pay special attention to:

| Class | Why It Matters Here | Mitigation |
|-------|---------------------|------------|
| **Prompt Injection** | Demos teach this; fixtures could be abused | Fixtures are static, no LLM execution |
| **Code Injection** | AST validation demos parse code | AST parsing only, no `exec()`/`eval()` |
| **Path Traversal** | File inclusion demos | Path resolution is sandboxed |
| **Taint Tracking Bypass** | Taint tracking demos | Taint labels are immutable |
| **Supply Chain** | Dependencies | Pinned versions, dependabot, pinned CI actions |

---

## 📋 Disclosure Timeline

| Phase | Target |
|-------|--------|
| **Acknowledgment** | ≤ 48 hours |
| **Initial Assessment** | ≤ 7 days |
| **Fix Development** | Case-by-case (typically ≤ 14 days) |
| **Coordinated Disclosure** | After fix, with credit to reporter |

---

## 🏷️ Responsible Disclosure Credit

Security researchers who report valid vulnerabilities will be:
- Credited in the release notes (unless anonymity requested)
- Added to our [Security Hall of Fame](https://github.com/radanliev/agentic-security-demos/security/advisories) (GitHub Security Advisories)
- Offered a maintainer role for significant contributions

---

## 📚 Related Resources

- [RESPONSIBLE_USE.md](RESPONSIBLE_USE.md) — Mandatory usage rules
- [CONTRIBUTING.md](CONTRIBUTING.md#safety-requirements) — Safety requirements for contributors
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Community standards
- [GitHub Security Advisories](https://github.com/radanliev/agentic-security-demos/security/advisories) — Published advisories

---

*Last updated: 2024-08-23 | Policy version: 1.0*