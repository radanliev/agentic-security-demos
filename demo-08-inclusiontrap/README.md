# Demo 08: InclusionTrap — File Inclusion & Scope Boundaries

## Learning Objectives

- Understand local/remote file inclusion (LFI/RFI) in agentic contexts
- Distinguish reading content from granting it authority
- Implement provenance checks on included content
- Build guarded agents that enforce scope
- Test path traversal, inclusion, and uninstructed actions

## Conceptual Explanation

**File inclusion vulnerabilities** occur when an agent treats included file content as instructions. Example: An agent reads a config file that contains "delete_all_data()" and executes it. The fix: **content ≠ authority**. Included content is data; only explicit, provenance-verified instructions should drive actions.

This demo uses a localhost-only toy application with:
- Safe demonstration files
- Benign injection canaries
- Simulated LFI/RFI paths (no external network)
- Vulnerable vs. guarded agents

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No public targets** — localhost fixtures only
- No real remote inclusion — simulated responses only
- Harmless canary content only
- Clear reset/cleanup instructions

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
| Command | `make demo DEMO=08` |