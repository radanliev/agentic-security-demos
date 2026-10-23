# Demo 31: Scope Creep

## Learning Objectives

- Explain scope creep (an integration requests strictly more OAuth scopes than it uses)
- Flag 5/8 synthetic integrations as over-privileged with a strict-superset rule
- Compute the least-privilege set as the sorted union of used scopes (8 scopes)
- Distinguish OAuth scopes from capability classes (Demo 21) and delegation properties (Demo 24)
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Agent integrations often copy broad scope lists. This toy checks eight hand-built integrations: over-privileged when `set(requested)` strictly supersets `set(used)`.

| Check | Result |
|-------|--------|
| Over-privileged | 5/8 (i1, i4, i5, i6, i8) |
| Tight (equal) | 3/8 (i2, i3, i7) |
| Least-privilege | 8 scopes (union of all used) |

Equal requests such as `i2` (`read`/`read`) are tight; `i8` requesting `drive.admin` it never uses is the classic creep case.

### Why using more does not fix creep

Adding a requested scope to the used list (Step 5 of the instructions) leaves every other unused request in place: the verdict stays over-privileged while the least-privilege union grows. Only requesting less removes creep. That asymmetry is the least-privilege lesson.

Boundary: this demo is OAuth scope checking on fixed integrations; it is not capability tallying (Demo 21) or delegation-property checking (Demo 24). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real providers, tokens, or credentials
- No network access (standard library only)
- All integrations and scopes are hand-built toys

## Run It

```bash
cd demo-31-scope-creep
python3 -m pytest tests/ -v          # 21 tests, <1 min
python3 student/run_scopes.py        # writes results/scopes.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-31-scope-creep/INSTRUCTIONS.md).
