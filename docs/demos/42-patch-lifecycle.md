# Demo 42: Patch Lifecycle

## Learning Objectives

- Explain the fix-to-adoption gap (a fix exists; deployments lag behind)
- Compute the median adoption lag over 8 synthetic vulns: exactly 37.5 days
- Show 2/8 fixes blocked by version pins
- Distinguish this teaching toy from the pending study it illustrates

## Conceptual Explanation

Fixing a library is only half the lifecycle; downstream stacks must adopt the fix. On 8 hand-built vulnerability records with adoption lags [5, 12, 20, 30, 45, 60, 90, 180] days:

| Statistic | Value |
|-----------|-------|
| Median adoption lag | (30 + 45) / 2 = 37.5 days |
| Blocked by version pin | 2/8 (vuln04, vuln07) |

The lesson: the median adopter waits over a month, and pins — not awareness — block a quarter of fixes. Both numbers are fixture properties, not ecosystem facts.

Boundary: this demo covers vulnerability lifecycle and adoption, not deployment config review (Demo 30). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real vulnerabilities, advisories, or credentials
- No network access (standard library only)
- All vulns, lags and verdicts are hand-built toys

## Run It

```bash
cd demo-42-patch-lifecycle
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_cycle.py         # writes results/lifecycle.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-42-patch-lifecycle/INSTRUCTIONS.md).
