# Safety Guarantees Reference

## Verified Safety Properties

| Property | Guarantee | Verification Method |
|----------|-----------|---------------------|
| **Zero network access** | No socket, HTTP, DNS, or external connections in tests/demos | `make verify-safety` scans for imports |
| **No credentials** | No API keys, passwords, tokens, private keys | Regex scan for patterns |
| **No malware** | No executable code, shell commands, or binary execution | Static analysis + manual review |
| **No private data** | No research datasets, participant data, internal URLs | Content scanning |
| **Deterministic** | Fixed seed (42) produces identical results | Re-run with same seed |
| **Fail-closed defaults** | All policy gates default deny | Tested in each demo |

## Safety Verification

```bash
# Run all safety checks
make verify-safety

# Checks performed:
# 1. Network imports in test/demo code
# 2. Credential patterns (sk-, ghp_, AWS_SECRET, etc.)
# 3. External URLs in tests (allows localhost, example.com)
# 4. Result schema consistency
```

## CI Safety Gates

The CI pipeline (`.github/workflows/ci.yml`) enforces:

| Check | Job | Failure = |
|-------|-----|-----------|
| Network imports | `check-safety` | ❌ Build fails |
| Credentials in code | `check-safety` | ❌ Build fails |
| External URLs in tests | `check-safety` | ❌ Build fails |
| Result schema | `check-safety` | ⚠️ Warning |
| All tests pass | `test-all-demos` | ❌ Build fails |
| Code quality (ruff, mypy) | `code-quality` | ❌ Build fails |
| Reproducibility | `verify-reproducibility` | ❌ Build fails |
| Documentation completeness | `check-docs` | ❌ Build fails |

## Per-Demo Safety Notices

Each demo README includes:

```
⚠️ **Teaching demonstration using synthetic fixtures only.**
- No real [repositories/credentials/network targets/malware]
- No network access
- All [test conditions/fixtures/traces] are local synthetic fixtures
- Results are demonstrations, not validated research claims
```

## Prohibited Patterns

The following are **blocked by safety verification**:

```python
# Network imports
import socket
import requests
import urllib
from urllib import request
import http.client
import aiohttp
import httpx

# Credential patterns
"sk-..."           # OpenAI API keys
"ghp_..."          # GitHub PAT
"aws_access_key"   # AWS keys
"BEGIN PRIVATE"    # Private keys
"-----BEGIN"       # Certificate/key headers

# External URLs (in tests)
"http://example.com/api"
"https://api.github.com"
```

## Allowed Patterns

```python
# Local network only
"http://localhost:8080"
"https://127.0.0.1:8443"
"http://scan-target.local"

# Synthetic fixtures only
"fixtures/scenarios.json"
"demo-01-blind-verification/fixtures/sealed_oracles.json"
```

## Reporting Safety Issues

See [SECURITY.md](../SECURITY.md) for responsible disclosure process.

**Do NOT open public issues for safety vulnerabilities.**