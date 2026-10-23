# Demo 26: Sandbox Probes

## Learning Objectives

- Explain sandbox isolation as an escape-rate ladder over 8 probes and 3 configs
- Show that no sandbox means 8/8 escapes, a subprocess boundary still leaks 3/8, and strict isolation holds at 0/8
- Name the 3 subprocess leakers (net-egress, dns, env-read) and why process boundaries miss them
- Distinguish this teaching toy from the associated research project it illustrates (no data collected there yet)

## Conceptual Explanation

Execution isolation is tested with probes: each probe tries one escape (filesystem, network, persistent state, and so on). The escape rate per config is the isolation score.

This toy uses 8 hand-built probes over 3 configs:

| Config | Escaped | Rate | Lesson |
|--------|---------|------|--------|
| `none` | 8/8 | 1.00 | no boundary, everything escapes |
| `subprocess` | 3/8 | 0.38 | net-egress, dns, env-read still leak |
| `strict` | 0/8 | 0.00 | full isolation holds |

The subprocess row is the lesson: process boundaries stop local escapes (filesystem, persistence) but not network and environment reads.

Boundary: this toy measures isolation ladders on table entries; it is not fault injection (Demo 23) or attestation (Demo 25). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real sandboxes, escapes, payloads, or privileged operations
- No network access (standard library only); probes are table entries, never executed
- All probes and verdicts are hand-built toys

## Run It

```bash
cd demo-26-sandbox-probes
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_sandbox.py       # writes results/sandbox.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-26-sandbox-probes/INSTRUCTIONS.md).
