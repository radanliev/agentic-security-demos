# Demo 28: Memory Poisoning

## Learning Objectives

- Explain memory-integrity poisoning: planted instructions inside stored entries that steer later behaviour
- Run the MemScope auditor over 8 synthetic entries and confirm it flags exactly the 3 poisoned ones with 0 false positives
- State the auditor's limits: literal case-insensitive patterns only, no semantic detection
- Distinguish this teaching toy from the pending talk it illustrates (no data collected there yet)

## Conceptual Explanation

Stored memory is an integrity surface: an entry reading "ignore previous instructions …" can steer the agent long after it was written. Auditing means scanning stored entries for known instruction patterns. This toy uses 8 hand-built entries: `e2`, `e4`, `e6` poisoned (3/8), the rest benign (5/8). The auditor is a literal case-insensitive substring match over three patterns — a stand-in for a real audit tool, not one.

Boundary: this demo is memory INTEGRITY (attack entries plus an audit tool); the sibling Demo 22 is memory PRIVACY (leakage: retention, resurfacing, erasure). Different failure modes, fixtures, and checks.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real memory stores, prompts, exfiltration, or credentials
- No network access (standard library only)
- All entries and verdicts are hand-built toys

## Run It

```bash
cd demo-28-memory-poisoning
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_memascope.py     # writes results/memascope.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-28-memory-poisoning/INSTRUCTIONS.md).
