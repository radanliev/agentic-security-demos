# Demo 24: Delegation Checks

## Learning Objectives

- Explain the two delegation properties: audience binding (one audience per chain) and no scope amplification (scope never grows)
- Check 6 synthetic delegation chains and read which two violate which property (4 clean, 2 violations)
- Distinguish delegation-property checking from OAuth scope measurement (the topic of Demo 31)
- Distinguish this teaching toy from the pending study it illustrates (no data collected there yet)

## Conceptual Explanation

When agents delegate — user to agent to tool — each hop carries a scope and an audience. Two properties must hold: every hop must name the same audience, and scope must never increase along the chain.

This toy uses 6 hand-built chains:

| Chains | Verdict | Lesson |
|--------|---------|--------|
| `c1`–`c4` | clean | both properties hold |
| `c5` | audience mismatch at hop 2 | audience flips `shop` → `evil` |
| `c6` | scope amplification 2→5 | downstream hop gains authority |

Chain `c3` is the contrast: a three-hop chain that stays clean.

Boundary: this demo checks delegation properties on fixed chains; it is not OAuth scope measurement (Demo 31) and not a formal protocol analysis. Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real principals, tokens, scopes, or authorisation servers
- No network access (standard library only)
- All chains and verdicts are hand-built toys

## Run It

```bash
cd demo-24-delegation-checks
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_authz.py         # writes results/authz.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-24-delegation-checks/INSTRUCTIONS.md).
