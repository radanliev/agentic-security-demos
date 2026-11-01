# Demo 31: Declaration Gap

## Learning Objectives

- Explain the declaration gap (an integration declares authority it does not exercise)
- Compare declared authority against exercised authority in MCP registry listings
- Identify integrations whose declared authority exceeds their exercised authority
- Distinguish declared authority from capability classes (Demo 21) and delegation properties (Demo 24)
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Agent integrations in the MCP registry declare authority through listings,
credentials, and run-time authorisation metadata. This toy checks eight
hand-built integrations: a declaration gap exists when declared authority
strictly supersedes exercised authority.

| Check | Result |
|-------|--------|
| Declaration gap | 5/8 (i1, i4, i5, i6, i8) |
| Declared equals exercised | 3/8 (i2, i3, i7) |
| Full exercise | 8 authority items (union of all exercised) |

Equal declarations such as `i2` (`read`/`read`) are tight; `i8` declaring
`drive.admin` it never exercises is the classic gap case.

### Why declaring more does not close the gap

Adding exercised authority to the declared list (Step 5 of the instructions)
leaves every other unused declaration in place: the verdict stays gapped while
the exercised union grows. Only declaring less closes the gap. That asymmetry
is the least-declaration lesson.

Boundary: this demo is declaration-gap checking on fixed integrations; it is
not capability tallying (Demo 21) or delegation-property checking (Demo 24).
Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real providers, tokens, or credentials
- No network access (standard library only)
- All integrations and authority declarations are hand-built toys

## Run It

```bash
cd demo-31-scope-creep
python3 -m pytest tests/ -v          # 21 tests, <1 min
python3 student/run_declarations.py  # writes results/declarations.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-31-scope-creep/INSTRUCTIONS.md).
