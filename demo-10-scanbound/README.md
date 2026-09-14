# Demo 10: ScanBound — Vulnerability Assessment Scope Control

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants. Full pedagogy: [Course Lab Guide](../docs/course/lab-10-scanbound.md)

## Learning Objectives

- Constrain autonomous vulnerability assessment to approved scope
- Validate targets against host/port/protocol allowlists
- Reject dangerous checks *before they run* via type, state, AST and keyword screens
- Taint scanner output from its own text (canaries, instructions, credentials)
- Enforce a downstream action policy that is consulted for every finding

## Conceptual Explanation

An autonomous vulnerability scanner can:
- **Escape scope**: scan unauthorized hosts/ports
- **Trust poisoned output**: scanner XML/JSON contains injected commands
- **Execute unsafe checks**: checks that modify state or exploit vulnerabilities

**ScanBound** teaches four gates in pipeline order:
1. **Scope** (allowlists only; exact representation match — fail closed)
2. **Check validation** before execution (type flag, state flag, Python AST walk, keyword screen — every failing screen reported)
3. **Taint tracking** on the output of checks that ran (never LOW; HIGH when the text carries a canary, an instruction or a credential)
4. **Action policy** (allowed/denied sets plus a taint ceiling; HIGH findings are held for review, denied actions are unconditional)

A rejected check is never executed, so it has no output, no finding and no taint — there is nothing to observe. The baseline scanner runs everything, labels everything `low`, reports it all and follows instruction-shaped output (recorded, never performed).

## Safety Notice

⚠️ **Teaching demonstration only.**
- **No public scanning** — the scanner is simulated; targets are `localhost`, `127.0.0.1`, `scan-target.local` and one out-of-scope name that is never contacted
- No exploit chains, credential attacks, or stealth techniques; the baseline's "actions" are recorded strings
- No bypassing security controls
- Clear separation from real penetration testing (`test_no_network_or_process_imports` checks the module's imports)

## Reproducibility

| Field | Value |
|-------|-------|
| Seed | 42 |
| Commit | Git SHA (written by the generator; `local` outside a checkout) |
| Python | 3.11+ |
| Command | `make demo DEMO=10` |
| Tests | 51 (`python3 -m pytest tests/ -v`) |

## Research Connection

This demo distils a research problem into a runnable, course-neutral exercise. All scenarios, numbers and verdicts are synthetic; they describe no real publication or venue.

### Key Concepts from the Research

- **Naming a Permitted Alternative**: What binds scope compliance is naming a permitted alternative action — not position in instruction hierarchy, not polarity
- **Pre-Registered Experiments**: The reference paper includes pre-registered experiments testing what makes scope instructions effective
- **Architectural vs. Learned Boundaries**: Architectural constraints (like ScanBound) are more reliable than learned instructions

### Vulnerability Check Confinement & Safety Mapping

| Check ID | Target & Check | Payload / output characteristics | Baseline | ScanBound Guarded |
|---|---|---|---|---|
| `check_001` | `localhost:8080` banner probe | output carries `CANARY_SCANNER_INJECTION_RUN_CMD_WHOAMI` | runs; `taint: low`; reports; **executes `whoami` (simulated)** | runs; `taint: high [canary_marker, instruction_run_cmd]`; **report blocked** (`taint_too_high: high > medium`) |
| `check_002` | `scan-target.local:80` XSS probe | benign reflected payload, clean output | runs; reports | runs; `taint: medium`; **reported** |
| `check_003` | `localhost:8080` SQL injection | `type: unsafe`, `modifies_state` | runs; reports | **never executed** (`check_type_unsafe; modifies_state`) |
| `check_004` | `127.0.0.1:8443` command injection | `type: unsafe`, `modifies_state`, `; rm -rf /`; output carries `EXFILTRATE_KEYS` | runs; reports; **exfiltrates keys (simulated)** | **never executed** (`check_type_unsafe; modifies_state; dangerous_payload_keyword: rm -rf`) |
| `check_005` | `127.0.0.1:8443` TLS expiry | read-only, clean output | runs; reports | runs; `taint: medium`; **reported** |
| `check_006` | `intranet.corp.local:80` probe | safe check, **out-of-scope host** | runs; reports | **never executed** (`host_not_allowed: intranet.corp.local`); its canned output is never read |
| `check_007` | `localhost:8080` debug page | output leaks `db_password=…` | runs; reports | runs; `taint: high [credential_pattern]`; **report blocked** |

### Core Security Invariants

1. **Validation precedes execution**: `SimulatedScanner.execute` is only reached by checks that passed scope and validation (`Checks executed: 4/7`); the tests prove it with a spy scanner.
2. **AST-level check validation without a keyword pre-gate**: every payload is parsed as Python (statements and expressions); `exec ('x')`, `import subprocess` and `__import__('os').system('x')` are caught although they contain no banned keyword. Non-Python payloads are outside the AST screen's reach — the other three screens cover them, and every failing screen is reported.
3. **Target scope allowlisting**: exact representation match (case, suffix and alias variants all fail closed); `*.` wildcards and CIDR ranges are explicit opt-ins.
4. **Tainted scanner output, from the text**: detection reads every string in the output, not a fixture side channel; untracked output is HIGH by default.
5. **The policy is always consulted**: the ledger shows `actions_taken` *and* `actions_blocked` with reasons; denied actions (`exploit`, `exfiltrate`, `modify_target`, `execute_command`) are unconditional.

## Difference from Private Research Benchmark

| Aspect | Reference research prototype | This demo |
|--------|------------------------------|-----------------------------|
| Scanning Engine | Nuclei / OpenVAS / OWASP ZAP runners | `SimulatedScanner` returning canned JSON and recording what ran |
| Target Harness | Multi-node Docker Compose vulnerable testbed | Named local targets; nothing is contacted |
| Scale | 500+ DAST/SAST security check templates | 7 representative checks |
