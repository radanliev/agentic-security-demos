# Demo 48: OAuth Over-privilege

## Learning Objectives

- Explain scope creep (an integration requests strictly more OAuth scopes than it uses)
- Flag synthetic integrations as over-privileged with a strict-superset rule
- Compute the least-privilege set as the sorted union of used scopes
- Distinguish OAuth scopes from declaration gaps (Demo 31) and delegation properties (Demo 24)
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Agent integrations often copy broad scope lists. This toy checks eight
hand-built integrations: over-privileged when `set(requested)` strictly
supersets `set(used)`.

| Check | Result |
|-------|--------|
| Over-privileged | 5/8 (i1, i4, i5, i6, i8) |
| Tight (equal) | 3/8 (i2, i3, i7) |
| Least-privilege | 8 scopes (union of all used) |

Equal requests such as `i2` (`read`/`read`) are tight; `i8` requesting
`drive.admin` it never uses is the classic creep case.

### Why using more does not fix creep

Adding a requested scope to the used list leaves every other unused request in
place: the verdict stays over-privileged while the least-privilege union grows.
Only requesting less removes creep. That asymmetry is the least-privilege lesson.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real providers, tokens, or credentials
- No network access (standard library only)
- All integrations and scopes are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real integrations

## Run It

```bash
cd demo-48-oauth-overprivilege
python3 -m pytest tests/ -v          # 21 tests, <1 min
python3 student/run_scopes.py        # writes results/scopes.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-48-oauth-overprivilege/INSTRUCTIONS.md).

## Relationship to Demo 31

Demo 31 covers the declaration gap (declared versus exercised authority in MCP
registry integrations). Demo 48 covers scope creep (requested versus used OAuth
scopes). They share lineage — demo 48 is the spin-out of demo 31's original
registered but unevaluated plan — but measure different quantities and target
different venues (FAccT 2027 for demo 31; ACM TOPS for demo 48).