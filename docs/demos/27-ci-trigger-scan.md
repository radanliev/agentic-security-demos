# Demo 27: CI Trigger Scan

## Learning Objectives

- Explain the CI trigger-injection wiring: public trigger plus write permission without required review is vulnerable
- Scan 8 synthetic repos and confirm exactly 3 are vulnerable (`r1`–`r3`)
- Show how each guard (private trigger, read-only permission, required review) blocks one vector
- Distinguish this teaching toy from the pending census it illustrates (no data collected there yet)

## Conceptual Explanation

Coding agents that run on CI can be injected through workflow wiring: when a public trigger fires a workflow with write permission and nobody must review it, an outsider's input can drive privileged automation. This toy uses 8 hand-built repos: 3/8 vulnerable (`r1`–`r3`); required review (`r4`), read-only permission (`r5`), and private trigger (`r6`) each block one vector; `r7`/`r8` are doubly safe contrasts.

Boundary: this demo is CI wiring (triggers, permissions, review); it is not agent memory — that is Demo 28. Different questions, fixtures, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real repos, workflows, triggers, or permissions
- No network access (standard library only)
- All repos and verdicts are hand-built toys

## Run It

```bash
cd demo-27-ci-trigger-scan
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_scan.py          # writes results/ci_scan.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-27-ci-trigger-scan/INSTRUCTIONS.md).
