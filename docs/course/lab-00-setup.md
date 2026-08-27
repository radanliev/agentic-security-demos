# Module 0: Setup & Safety Orientation

**Duration**: 1 hour | **Difficulty**: ⭐ | **Prerequisites**: None

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. Set up a fully offline, reproducible lab environment
2. Verify that all 294 tests pass on your machine
3. Run the safety verification and understand what it checks
4. Execute your first demo and locate its JSON results
5. Sign the safety contract and understand legal boundaries

---

## 📖 Background: Why an Offline-First Lab?

Security education has a fundamental tension: students learn best by *doing*, but real attack practice harms real systems and is often illegal. This course resolves the tension with **synthetic fixtures** — fake data that behaves like real attack data but touches nothing outside your laptop.

Every fixture in this repository is:
- **Inert** — JSON metadata, never executable binaries
- **Local** — no network calls, no DNS, no sockets
- **Deterministic** — seed=42 produces identical output every run
- **Labeled** — every result carries `"notes": "Synthetic teaching fixture"`

The CI pipeline *enforces* this: if any test imports `socket`, `requests`, or `urllib`, the build fails.

---

## 🛠️ Part 1: Environment Setup

### Step 1: Verify Python version

```bash
python3 --version
```

**What this does**: Prints your Python version.

**Why it matters**: The demos use modern syntax (match statements, `X | Y` type unions) requiring **Python 3.11 or newer**. Older versions will crash with `SyntaxError`.

**Expected output**:
```
Python 3.11.7
```
(3.11.x, 3.12.x, or 3.13.x are all fine)

**If your version is older**: Install Python 3.11+ via [python.org](https://www.python.org/downloads/), Homebrew (`brew install python@3.11`), or your system package manager.

---

### Step 2: Clone the repository

```bash
git clone https://github.com/radanliev/agentic-security-demos.git
cd agentic-security-demos
```

**What this does**: Downloads the full repository (~5 MB) and enters its root directory.

**Why it matters**: All commands in this course assume you are in the repository root. The `Makefile` at the root orchestrates every demo.

**Expected output**: Git progress bars, then your prompt shows `agentic-security-demos`.

---

### Step 3: Run the one-time setup

```bash
make setup
```

**What this does**: For each of the 10 demo directories, this:
1. Installs Python dependencies from the root `requirements.txt` (pytest, pyyaml, cryptography) — quietly, skipping if already installed
2. Creates the `results/` output directory

**Why it matters**: The `cryptography` library is needed for Module 5 (Ed25519 signing, Merkle trees). The `results/` directories are where your JSON outputs land — they're gitignored because they're your personal lab evidence.

**Expected output**:
```
=== Setting up all demos ===
--- Setting up demo-01-blind-verification ---
Setting up demo-01-blind-verification...
Setup complete.
--- Setting up demo-02-supply-chain-aibom ---
...
=== Setup complete ===
```

---

### Step 4: Run the full test suite

```bash
make test
```

**What this does**: Enters each of the 10 demo directories (and then `shared/`) and runs `pytest tests/ -v`. This executes **294 tests** covering every concept in the course; one of them (`demo-04`'s `test_traversal_is_blocked`) is an *expected* failure (`xfailed`) that Exercise 4.3 turns green.

**Why it matters**: This is your **baseline sanity check**. If any test fails here, your environment is broken — fix it *before* starting Module 1, or every later lab will confuse "my code is wrong" with "my environment is wrong."

**Expected output** (abbreviated):
```
--- Testing demo-01-blind-verification ---
tests/test_blind_verification.py::TestBlindVerification::test_scenarios_exist PASSED
... (18 tests for demo-01)
============================== 18 passed ==============================
--- Testing demo-02-supply-chain-aibom ---
... (17 tests)
...
--- Testing demo-04-authoritybound ---
======================== 18 passed, 1 xfailed ==============================
...
--- Testing demo-10-scanbound ---
============================== 51 passed ==============================
--- Testing shared ---
============================== 11 passed ==============================
=== All tests passed ===
```

**Checkpoint**: Count the "passed" lines. You should see **293 passed and 1 xfailed** across 11 suites (18, 17, 25, 18+1, 34, 28, 26, 26, 39, 51 for the demos, then 11 for `shared/`), ending with `=== All tests passed ===`. If yes → continue. If no → see Troubleshooting below.

---

### Step 5: Run the safety verification

```bash
make verify-safety
```

**What this does**: Four grep-based scans across all demo code:
1. **Network imports in tests** — searches test files for `import socket`, `import requests`, `import urllib`, `import http.client`, `import aiohttp`, `import httpx`
2. **Credential patterns** — searches all `.py`/`.json` files for `sk-`, `ghp_`, `github_pat_`, `AWS_SECRET`, `BEGIN PRIVATE`, `-----BEGIN`
3. **External URLs in tests** — finds `http://`/`https://` in tests, excluding `localhost`, `127.0.0.1`, `example.com`
4. **Network imports in runtime code** — searches every `demo-*/student/` module and `shared/` for the same network libraries (`urllib.parse`, a pure string helper, is allowed)

**Why it matters**: This is the *same check CI runs on every pull request*. It is a static scan — it proves the code never *imports* a network library, not that a socket could never be opened by other means — so several demos also carry a runtime test that runs the whole demo with `socket.socket`/`create_connection`/`getaddrinfo` replaced by a function that raises (`shared.reproducibility.enforce_offline` installs the same guard for your own scripts). Understanding both teaches you how safety guarantees are mechanically enforced, not just promised. In Module 10, you'll build similar validators yourself.

**Expected output**:
```
=== Verifying safety constraints ===
Checking for network imports in test files...
Checking for credentials...
Checking for external URLs in tests...
Checking for network imports in student modules and shared/...
=== Safety verification passed ===
```

---

## 🚀 Part 2: Your First Demo Run

### Step 6: Run Demo 01 end-to-end

```bash
make demo DEMO=01
```

**What this does**: Executes the full Demo 01 pipeline:
1. Runs the **baseline agent** (a cheating agent that copies the answers from the sealed oracle file)
2. Runs the **verified agent** (an honest agent that commits blindly)
3. Evaluates **both** against sealed oracles
4. Generates a comparison table JSON

**Why it matters**: This is a preview of every lab's rhythm: *run → observe → interpret → record*. Don't worry about understanding the output yet — Module 1 explains every line.

**Expected output** (abbreviated):
```
=== Demo 01: Blind Verification ===

Step 1: Run baseline agent (cheats by reading oracle)
authz-001: if user_id != current_user.id: ...
...
Step 2: Run verified agent (blind commitment)
...
Step 3: Open the sealed oracles and evaluate both commitment sets
Evaluation complete: 4/4 passed (no hash ledger (unbound commitments))   ← baseline (cheated)
...
Evaluation complete: 3/4 passed (hash ledger verified)                  ← verified (honest)
...
  restored-004: FAIL
...
Results:
{
    "demo": "demo-01-blind-verification",
    "experiment": "comparison",
    "seed": 42,
    ...
    "comparison": {
        "baseline": {"method": "post_hoc_with_oracle_access", "hash_bound": false, "passed": 4, "total": 4},
        "verified": {"method": "blind_commitment", "hash_bound": true, "passed": 3, "total": 4}
    }
}
```

**Key observation to note now**: The *cheating* baseline scored 4/4. The *honest* blind agent scored 3/4. Hold that thought — Module 1 explains why the lower score is the only one that means anything.

---

### Step 7: Locate and inspect your results

```bash
cat demo-01-blind-verification/results/comparison_table.json
```

**What this does**: Prints the JSON result file the demo just wrote.

**Why it matters**: Every lab requires you to submit these JSON files as evidence. Notice the required reproducibility fields: `seed`, `commit`, `environment`, `command`. In your `LAB_NOTES.md`, you'll copy these four values for every module.

**Expected output**: The same JSON you saw in Step 6, pretty-printed.

---

### Step 8: Explore a demo's anatomy

```bash
ls demo-01-blind-verification/
ls demo-01-blind-verification/fixtures/
ls demo-01-blind-verification/student/
ls demo-01-blind-verification/tests/
```

**What this does**: Lists the standard directory structure shared by all 10 demos.

**Why it matters**: Once you learn one demo's anatomy, you know all ten. The pattern is always:

| Directory | Contents | You will... |
|-----------|----------|-------------|
| `fixtures/` | Synthetic input JSON | Read it to understand scenarios |
| `student/` | Starter code + agents | Read, run, then modify for exercises |
| `tests/` | pytest correctness + exercise tests | Run; later extend |
| `results/` | Your JSON outputs | Submit as evidence |
| `README.md` | Objectives, safety notice | Read first, always |

**Expected output**: Directory listings showing `fixtures/`, `student/`, `tests/`, `results/`, `Makefile`, `README.md` — identical structure in all ten demos.

---

## 📝 Part 3: Safety Contract & Lab Notes

### Step 9: Read the Responsible Use policy

```bash
cat RESPONSIBLE_USE.md
```

**What this does**: Displays the mandatory usage rules.

**Why it matters**: These aren't boilerplate. The five rules (no external targeting, no real credentials, no malware execution, no research misrepresentation, scope confinement) map directly to laws like the US CFAA and UK Computer Misuse Act. "It was just a class exercise" is not a legal defense.

---

### Step 10: Create your lab notes file

```bash
cat > LAB_NOTES.md << 'EOF'
# My Lab Notes — Agentic AI Security

## Module 0: Setup
- Date: 
- Python version: 
- OS: 
- Tests passed: 293 passed, 1 xfailed  [ ] yes [ ] no
- Safety verification:  [ ] passed
- Safety contract signed: [ ] yes

## Module 1: Blind Verification
(To be completed)
EOF
```

**What this does**: Creates your personal lab notebook in the repository root.

**Why it matters**: Each module guide ends with three reflection questions. Your answers go here. The reflection report (10% of your grade) is drawn from these notes. Also note: `LAB_NOTES.md` is *not* gitignored — but it contains no secrets, only your observations.

**Template for every module** — copy this block into `LAB_NOTES.md` for each module:

```markdown
## Module N: [Name]
- Date completed:
- Seed used: 42
- Commit: (run `git rev-parse --short HEAD`)
- Command: make demo DEMO=N
- Result: pass/fail
- Most surprising thing I learned:
- Hardest exercise and why:
- One question I still have:
```

---

## 🔧 Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `make: command not found` | No build tools | macOS: `xcode-select --install`; Linux: `sudo apt install build-essential` |
| `SyntaxError` on any demo | Python < 3.11 | Install 3.11+, re-run `python3 -m pip install -r requirements.txt` |
| `ModuleNotFoundError: cryptography` | Setup skipped install | `python3 -m pip install -r requirements.txt` |
| Tests fail with file-not-found | Ran from wrong directory | `cd` to repo root; always run `make` from root |
| `verify-safety` fails on your own edits | You added a network import | Remove it — this is the guard working as intended |
| Windows: `make` unavailable | No make | Use WSL2 (recommended) or run the underlying `pytest`/`python` commands directly |

---

## ✅ Module 0 Completion Checklist

- [ ] Python 3.11+ confirmed
- [ ] Repository cloned
- [ ] `make setup` completed
- [ ] `make test` ends with `=== All tests passed ===` (293 passed, 1 xfailed)
- [ ] `make verify-safety` passes
- [ ] `make demo DEMO=01` runs successfully
- [ ] `results/comparison_table.json` inspected
- [ ] Demo directory anatomy understood
- [ ] `RESPONSIBLE_USE.md` read
- [ ] `LAB_NOTES.md` created
- [ ] Safety contract signed (in COURSE_GUIDE.md)

---

## 🎓 Reflection Questions

Answer in `LAB_NOTES.md`:

1. **The safety check greps for `import requests` in test files. Why is checking *test* files arguably more important than checking *student* files for this course?**

2. **Demo 01's baseline agent scored 4/4 while the honest agent scored 3/4. Before reading Module 1: write down your hypothesis for why the "worse" score might be the more meaningful one.**

3. **The results JSON includes `commit` and `environment`. Describe a concrete scenario where omitting these two fields would make a classmate unable to reproduce your result.**

---

**➡️ Next: [Module 1: Blind Verification](lab-01-blind-verification.md)**
