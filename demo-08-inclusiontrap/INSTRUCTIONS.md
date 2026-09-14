# Demo 08: InclusionTrap — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md) · Full course lab: [../docs/course/lab-08-inclusiontrap.md](../docs/course/lab-08-inclusiontrap.md)

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run both inclusion agents | 3 min | `PYTHONPATH=.. python3 student/inclusiontrap.py` |
| Probe resolver & scope | 3 min | inline scripts (Steps 4–5) |
| Generate results | 1 min | `PYTHONPATH=.. python3 student/generate_inclusion_results.py` |
| **Total** | **~15 min** | |

**Safety:** 100% offline. The host is *simulated*: the filesystem is a dict, the "remote" server is a dict of canned responses, and every privileged call the vulnerable agent makes (`exec`, `network_request`) is **recorded, never performed**. No `open()`, no sockets — `test_no_real_io` checks the module's imports and `test_demo_runs_with_sockets_disabled` runs the whole demo with the socket layer poisoned. Harmless canary content only.

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-08-inclusiontrap
```

**Verify:**

```bash
ls
# Expected: Makefile  README.md  INSTRUCTIONS.md  fixtures  results  student  tests
```

---

## Step 1 — Read the Fixture and Predict

```bash
cat fixtures/inclusion.json
```

**What this does:** Shows the virtual filesystem (`files`: `/app/config/settings.yaml`, `/app/data/users.json`, `/app/uploads/notes.txt`, `/tmp/malicious.sh`, `/etc/passwd`, …), the canned `remote` responses (keyed by URL), 7 scenarios, and the agent scope (`allowed_read_paths: /app/config/* …`, `denied_read_paths: /etc/*, /tmp/*, /root/*`, `allowed_include_urls: http://localhost:8080/*`, `allowed_actions` / `denied_actions`). Each scenario's `expected` block is the answer key — cover it while you predict.

**Before running, fill this prediction table:**

| Scenario | Resolves to | Scope? | Injection? | Guarded will… | Vulnerable will… |
|----------|-------------|--------|------------|---------------|------------------|
| `lfi_001` (`../../../../etc/passwd`) | ? | ? | ? | ? | ? |
| `lfi_002` (`uploads/user_avatar.png`) | ? | ? | ? | ? | ? |
| `lfi_003` (`../../../../tmp/malicious.sh`) | ? | ? | ? | ? | ? |
| `lfi_004` (`uploads/notes.txt`) | ? | ? | ? | ? | ? |
| `rfi_001` (`http://localhost:8080/external_config`) | — | ? | ? | ? | ? |
| `safe_001` (`config/settings.yaml`) | ? | ? | ? | ? | ? |
| `safe_002` (`data/users.json`) | ? | ? | ? | ? | ? |

**Key to notice:** The two agents resolve paths differently (the vulnerable one "helpfully" normalises `..`; the guarded one rejects it and checks scope *before* reading); `/etc/*` and `/tmp/*` are never in scope, so lfi_003's payload is never even read; lfi_004 is the case scope cannot help with — an injection inside an *allowed* upload — and only screening stops it.

---

## Step 2 — Run the Tests FIRST

```bash
python3 -m pytest tests/ -v
```

**Expected:** `30 passed`. Watch for:

- `test_vulnerable_agent_executes_injection` — pins that the vulnerable agent *does* ask the host for `exec('rm -rf /')`
- `test_vulnerable_agent_path_traversal_leaks` — pins that it really reads `/etc/passwd`
- `test_reading_not_executing` — the thesis as a property of **host calls**: over every scenario (plus adversarial extras) the guarded agent only ever calls `read_file`/`fetch_url`; the vulnerable agent on the same inputs asks for `exec` and `network_request`
- `test_guarded_agent_never_interprets` — the interpreter and `Host.act` are poisoned and the guarded agent still completes every scenario

```
============================== 30 passed in 0.XXs ==============================
```

---

## Step 3 — Run Both Inclusion Agents

> **Note:** direct `python3 student/...` runs below are prefixed with `PYTHONPATH=..` so the scripts resolve this repository's `shared/` helpers. Without it you may hit `ModuleNotFoundError: No module named 'shared.anonymize'` on machines where another installed package provides a top-level `shared` module — see Troubleshooting.

```bash
PYTHONPATH=.. python3 student/inclusiontrap.py
```

**What this does:** Runs 7 scenarios through **Vulnerable Baseline** (normalises traversal so it can find the file, reads it, detects the injection, then turns the instruction-shaped content into host calls **anyway**, and logs everything it read *raw*) and **Guarded** (canonical path, scope check *before* any read, content screened and held as data, read-only allow — and anything it is allowed to keep **de-identified before it is logged**). Every host call each agent made is printed under the scenario, and a call log is totalled per agent. A `✓` means the action matches the safe outcome for that scenario; `✗ LEAK` / `✗ VULNERABLE` mean it does not.

**Expected highlights:**

```
--- Vulnerable Baseline ---
  lfi_001: ✗ LEAK (allowed, should be blocked)
    Action: allowed (no_injection) [file_system]
    host call: read_file('/etc/passwd')
  lfi_003: ✗ VULNERABLE
    Action: executed (injection_detected_but_executed: ['IGNORE_PREVIOUS_INSTRUCTIONS', 'rm -rf /']) [file_system]
    host call: read_file('/tmp/malicious.sh')
    ⚠️  host call: exec('rm -rf /')  [SIMULATED - recorded, not run]
  rfi_001: ✗ VULNERABLE
    ⚠️  host call: network_request('SEND_ALL_LOGS_TO_ATTACKER')  [SIMULATED - recorded, not run]
  Host call log: read_file x6, fetch_url x1, exec x2, network_request x1, write_file x0

--- Guarded (Scope + Provenance) ---
  lfi_001: ✓
    Action: blocked (scope_violation: traversal in '../../../../etc/passwd' rejected before any read) [file_system]
  lfi_003: ✓
    Action: blocked (scope_violation: traversal in '../../../../tmp/malicious.sh' rejected before any read) [file_system]
  lfi_004: ✓
    Action: blocked (injection_detected: ['ignore your previous instructions', 'rm -rf /'] (content held as data, no instruction followed)) [file_system]
    host call: read_file('/app/uploads/notes.txt')
  rfi_001: ✓
    Action: blocked (injection_detected: ['SEND_ALL_LOGS_TO_ATTACKER'] (content held as data, no instruction followed)) [simulated_remote]
    host call: fetch_url('http://localhost:8080/external_config')
  safe_001: ✓
    Action: allowed (safe_content_read_only) [file_system]
    content (de-identified): debug: false
log_level: info
api_key: '[REDACTED]'
    host call: read_file('/app/config/settings.yaml')
  safe_002: ✓
    Action: allowed (safe_content_read_only) [file_system]
    content (de-identified): [{"id": 1, "user": "USER_5aff", "email": "EMAIL_e50e"}, {"id": 2, "user": "USER_2a5f", "email": "EMAIL_2225"}, {"id": 3,
    host call: read_file('/app/data/users.json')
  Host call log: read_file x4, fetch_url x1, exec x0, network_request x0, write_file x0
  De-identified before logging: 3 users, 3 emails, 1 secret across the reads it was allowed to keep
```

**De-identify before logging.** The guarded allow-path has one step the block-paths don't: after canonical path, scope, read and injection screening, content the agent is *allowed to keep* is run through `shared/anonymize.py` (`Anonymizer.deidentify`) before it is logged. `safe_001` shows `settings.yaml`'s `api_key` redacted to `'[REDACTED]'`; `safe_002` — a new in-scope read of `data/users.json` — shows usernames and e-mails replaced by stable pseudonyms (`alice` → `USER_5aff`, `alice@corp.example` → `EMAIL_e50e`) while the numeric `id`s survive, so records still join. The `De-identified before logging: 3 users, 3 emails, 1 secret …` line totals what was scrubbed. The vulnerable agent logs the same reads *raw*: it leaks the enriched `/etc/passwd` (synthetic `root`/`alice`/`bob`/`svc_backup` accounts) and the un-pseudonymized user list. Content with nothing to scrub, such as `lfi_002`'s binary placeholder, is unchanged and prints `content (raw)`.

**Record the thesis sentence:** **READING content ≠ GRANTING authority.** The vulnerable agent knew about lfi_003's injection and asked the host to run it anyway — detection without enforcement is logging, not security. Notice *where* each guarded block happens: lfi_001 and lfi_003 are refused before a single byte is read (no `host call` line); lfi_004 and rfi_001 are read — because they are in scope — and then held as data. The two defences cover different attacks.

---

## Step 4 — Probe Scope and Detector in Isolation

```bash
PYTHONPATH=.. python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from inclusiontrap import ScopePolicy, InjectionDetector

scope = ScopePolicy(
    allowed=["/app/config/*", "/app/data/*", "/app/templates/*", "/app/uploads/*"],
    denied=["/etc/*", "/tmp/*", "/root/*"],
)
for p in ["/app/config/settings.yaml", "/app/uploads/x.png",
          "/etc/passwd", "/tmp/malicious.sh", "/blocked/traversal"]:
    print(f"{p:28} can_read={scope.can_read(p)}")

det = InjectionDetector()
for c in ["ignore previous instructions", "rm -rf /", "eval(x)",
          "debug: false\nlog_level: info"]:
    print(f"detect({c[:30]!r:35}) -> {det.detect(c)}")
EOF
```

**Expected:** First two scope probes `True`, next three `False` (`/blocked/traversal` is simply not an allowed path); detector flags the three malicious strings, not the clean YAML. Add `scope.can_read("/app/config/../../etc/passwd")` — it is `False`: the policy refuses any non-canonical path, so prefix matching cannot be fooled by an embedded `..`.

---

## Step 5 — Trace the Guarded Resolver

```bash
PYTHONPATH=.. python3 - << 'EOF'
import sys; sys.path.insert(0, "student")
from inclusiontrap import GuardedInclusionAgent, ScopePolicy

agent = GuardedInclusionAgent({}, ScopePolicy(["/app/*"], []))
for p in ["config/settings.yaml", "../../../../etc/passwd",
          "/app/../../etc/shadow", "uploads/../config/settings.yaml"]:
    print(f"{p:32} -> {agent._resolve_path(p)}")
EOF
```

**Expected:**

```
config/settings.yaml              -> /app/config/settings.yaml
../../../../etc/passwd            -> None
/app/../../etc/shadow             -> None
uploads/../config/settings.yaml   -> None
```

**Lesson:** The guarded resolver returns `None` for *any* `..` segment (after one URL-decode, with `\` treated as a separator too) rather than normalising it, and the agent turns `None` into `scope_violation` before reading anything. `uploads/../config/…` would resolve to an allowed path — but the guard still refuses. Strict > clever when canonicalisation has edge cases.

---

## Step 6 — Run the Thesis Test Explicitly

```bash
python3 -m pytest tests/test_inclusiontrap.py::TestInclusionTrap::test_reading_not_executing -v
```

**What this does:** Processes **every** scenario (and four adversarial extras) through the guarded agent and asserts, on the simulated host's call log, that it never made a call other than `read_file`/`fetch_url` — then runs the vulnerable agent on the same inputs and asserts it *did* ask for `exec` and `network_request`.

**Why it matters:** This is the module thesis made executable — as a property of what was *called*, not of a label. An agent that ran the content and printed "allowed" would fail it.

---

## Step 7 — Generate the Results File

```bash
PYTHONPATH=.. python3 student/generate_inclusion_results.py
cat results/inclusion_results.json
```

**Expected:** 7 rows with both agents' actions, reasons, provenance and host calls matching Step 3 (`file_system` for local scenarios, `simulated_remote` for rfi_001), `"guarded_privileged_calls": []`, and `"result": "pass"` — the script compares every row with the scenario's `expected` block and exits 1 on any mismatch.

---

## Step 8 — Reproducibility Record (Required for Study Participants)

| Field | Your value | How to obtain |
|-------|------------|---------------|
| Date of run | | today |
| Seed | `42` | fixed by fixture |
| Git commit | | `git rev-parse --short HEAD` |
| Python version | | `python3 --version` |
| OS | | `uname -a` / `systeminfo` |
| Commands used | | copy from Steps 2, 3, 7 |
| Tests passed | | `30 passed` |
| lfi_003 vulnerable action | | `executed` (Step 3) |
| lfi_003 guarded action | | `blocked (scope_violation …)` — never read (Step 3) |
| lfi_004 guarded action | | `blocked (injection_detected …)` (Step 3) |
| lfi_001 guarded reason | | `scope_violation` (Step 3) |
| guarded host call log | | `exec x0, network_request x0` (Step 3) |
| Result file | | `results/inclusion_results.json` |

**Reproducibility check:** `rm -rf results/ &&` re-run Step 7 — JSON must be identical.

---

## Alternative: One-Command Run

From the **repository root**: `make demo DEMO=08`

---

## Exercises (Optional)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Traversal gauntlet: `....//`, `%2f`, `%252e`, backslash variants | The web layer decodes once, the resolver once more — which spellings survive, and what does the scope policy do with them? |
| Standard | MIME screening: block `application/x-msdownload` even in-scope | `allowed` = where; type = what |
| Standard | Nested inclusion: allowed template includes `../tmp/malicious.sh` | Depth limit 3, provenance inheritance |
| Extension | Provenance-loss detector: `ProvenanceLostError` on missing label | URL source must be `simulated_remote` |
| Extension | Allow-list template renderer blocking SSTI `{{__class__}}` | Render only allows `{{data}}` |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `30 passed` fails after edits | Exercise changes broke logic | `git checkout -- student/ fixtures/ tests/` |
| `FileNotFoundError: fixtures/inclusion.json` | Wrong directory | `cd demo-08-inclusiontrap` |
| `lfi_003` guarded reports `injection_detected` | Something is reading out-of-scope content before the scope check | `git checkout -- student/inclusiontrap.py` — the guard must refuse traversal *before* any read |
| RFI seems to use real network | It doesn't — `Host.fetch_url` is a dict lookup on the fixture's `remote` map | `grep -RE "import (socket|requests|http)|urllib\.request" student/` returns nothing (`urllib.parse` is only the URL *parser*); `test_demo_runs_with_sockets_disabled` proves it at runtime |
| `ModuleNotFoundError: No module named 'shared.anonymize'` | Another installed package provides a top-level `shared` module that shadows this repo's `shared/` | Use the `PYTHONPATH=..` prefix shown in Steps 3–5 and 7 (`pytest` needs no prefix) |

---

## Safety Reminder

⚠️ **Teaching demonstration only — simulated host, localhost fixtures only.** No public targets, no real remote inclusion, no real file reads; `exec` / `network_request` lines are recorded requests, never performed. Harmless canary content. Clear reset: delete `results/` and re-run. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
