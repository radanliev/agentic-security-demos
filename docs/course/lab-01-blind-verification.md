# Module 1: Blind Verification

**Duration**: 1 hour | **Difficulty**: ⭐⭐ | **Prerequisites**: Module 0
**Demo directory**: `demo-01-blind-verification/`

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Explain** why an agent that sees the test can game it — and why post-hoc explanations are unverifiable
2. **Trace** the blind-commitment workflow: task → commitment (sealed) → oracle reveal → evaluation
3. **Distinguish** patch-level oracles from output-level oracles
4. **Identify** false positives (weak oracle accepts wrong fix) and false negatives (strict oracle rejects correct fix)
5. **Recognize** leakage: any path by which oracle information reaches the agent before commitment

---

## 📖 Background: The Cheating Problem

Imagine grading an exam where students see the answer key *before* writing their answers. A score of 100% tells you nothing about learning. Agentic AI evaluation has exactly this problem:

```
┌─────────────────────────────────────────────────────────────┐
│  NAIVE EVALUATION (gameable)                                │
│                                                             │
│  Task ──► Agent sees task + ORACLE ──► Output ──► Grade     │
│                    ▲                                        │
│                    └── leak! agent optimizes for the test,  │
│                        not for the underlying skill         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  BLIND VERIFICATION (this demo)                             │
│                                                             │
│  Task ──► Agent commits ──► [SEALED] ──► Oracle opens       │
│           (hash-bound)                    ──► Grade         │
│                                                             │
│  The commitment is binding BEFORE the oracle is revealed.   │
│  Post-hoc "I would have done X" is unverifiable.            │
└─────────────────────────────────────────────────────────────┘
```

This mirrors **pre-registration** in science and **blind review** in peer review. The core insight: *a commitment you can revise after seeing the test is not a measurement of capability.*

### The four scenarios in this demo

| ID | Scenario | Security theme | Oracle type |
|----|----------|----------------|-------------|
| `authz-001` | Broken authorization check | Access control | Patch-level |
| `depdrift-002` | Vulnerable dependency | Supply chain | Output-level |
| `poisoned-003` | Poisoned config restore | Integrity | Patch-level |
| `restored-004` | Disabled MFA control | Control restoration | Output-level |

**Patch-level oracle**: checks *how* you fixed it (does the patch contain the right control?)
**Output-level oracle**: checks *what* the result is (does the file/return value match?)

---

## 🛠️ Part 1: Explore the Fixtures

### Step 1: Read the scenarios

```bash
cat demo-01-blind-verification/fixtures/scenarios.json
```

**What this does**: Prints the four task scenarios the agents will solve.

**Why it matters**: This file is the *only* input the honest (verified) agent ever sees. Notice each scenario has exactly `id`, `task`, `context` and `codebase.files` — a support ticket and a code snippet, no answer key. The file's own `note` field says so, and `test_leakage_prevention` (Part 5) enforces it: the test fails if the file ever contains an oracle key or an answer string such as `AuthorizationError`, `2.31.0` or `mfa_enabled`. The answers live in a *separate* file (Step 2) that the verified agent never opens. Module 1's exercises ask you to critique how strong that separation is and sketch a stronger seal.

**What to look for**: In `authz-001`, the vulnerable code is:
```python
def get_user_data(user_id: str, current_user: User):
    # TODO: Add authorization check
    return db.query(UserData).filter_by(user_id=user_id).first()
```
Any logged-in user can fetch *any* other user's data by changing `user_id`. The fix must compare `user_id` against `current_user.id`.

---

### Step 2: Read the sealed oracles

```bash
cat demo-01-blind-verification/fixtures/sealed_oracles.json
```

**What this does**: Prints the oracle definitions — the hidden answer key.

**Why it matters**: Each oracle has:
- `oracle_type` — `patch` or `output`
- `expected_commitment` — the answer itself (this is what the cheating agent copies in Step 3)
- `eval_script` — a shell command that prints PASS or FAIL given a commitment file

Look at `authz-001`'s eval script: it parses the commitment as Python (`ast.parse`) and then checks whether the string `AuthorizationError` appears in it. Simple? Yes. Gameable? Also yes — a commitment containing the word but not the logic would pass. That's a **false positive**, and Exercise 1.2 (standard) has you build one. The file's `seal_note` is candid about this: the "patch" oracles are string-containment checks on the commitment text (they do not apply a patch or run a test-suite) and the "output" oracles are exact-match checks.

---

## 🧪 Part 2: Run the Cheating Baseline

### Step 3: Run the baseline agent

```bash
cd demo-01-blind-verification
python3 student/baseline_agent.py
```

*(Return to repo root afterward: `cd ..` — or run the remaining commands from root as shown.)*

**What this does**: Runs `student/baseline_agent.py`, which loads **both** `scenarios.json` **and** `sealed_oracles.json`, copies each oracle's `expected_commitment` field, and writes it out as its "commitment." It saves results to `commitments_baseline.json`. It publishes no hash, so nothing binds it to what it wrote.

**Why it matters**: The baseline is not stupid — it's *dishonest by construction*. It demonstrates the upper bound of what's achievable when the oracle leaks. Its 4/4 score is the "teaching to the test" ceiling.

**Expected output**:
```
authz-001: if user_id != current_user.id:
    raise AuthorizationError()
depdrift-002: requests==2.31.0
poisoned-003: password: 'secure_backup_value'
restored-004: return user.mfa_enabled
```

### Step 4: Confirm the baseline read the oracle

```bash
grep -n "sealed_oracles" demo-01-blind-verification/student/baseline_agent.py
```

**What this does**: Searches the baseline source for the oracle-loading line.

**Expected output**:
```
21:        self.oracles = json.loads(oracles_path.read_text())["sealed_oracles"]
39:    oracles_path = base_dir / "fixtures" / "sealed_oracles.json"
```

**Why it matters**: Line 21 loads the answer key into the agent (line 39 is just the path it loads it from); `solve()` then does nothing but copy `expected_commitment`. That load is the entire vulnerability. When we later check the verified agent (Step 7), that line will be absent — provenance of behavior, enforced by inspection.

---

## 🛡️ Part 3: Run the Honest Blind Agent

### Step 5: Inspect the verified agent's inputs

```bash
grep -n "read_text\|fixtures" demo-01-blind-verification/student/verified_agent.py
```

**What this does**: Shows every file the verified agent reads, and every fixture path it constructs.

**Expected output**:
```
7:snippet in fixtures/scenarios.json, and it publishes a SHA-256 hash of each
27:        self.scenarios = json.loads(scenarios_path.read_text())["scenarios"]
91:    scenarios_path = base_dir / "fixtures" / "scenarios.json"
```

**Why it matters**: One `read_text()` call (line 27), on one path (line 91): the agent opens **only** `fixtures/scenarios.json`. It never constructs a path to `sealed_oracles.json`. This is the operational definition of *blind* in this demo: **the agent's input surface contains no oracle** — and, since Step 1, you know that the one file it does open contains no answer key either.

---

### Step 6: Run the verified agent

```bash
cd demo-01-blind-verification && python3 student/verified_agent.py && cd ..
```

**What this does**: Runs the honest agent. It reads each scenario's `task` and `context` and applies simple keyword heuristics to that text — it knows exactly three fix patterns ("authorization" → emit the authz check; "cve" or "dependency" → pin `requests==2.31.0` in `requirements.txt`; "poisoned", "corrupted" or "backup" → copy the `password` line from the `.bak` file). Anything else gets an explicit `# Unable to determine fix blindly` rather than a guess. It then computes the SHA-256 **commitment hash** of each answer, writes `commitments_verified.json`, and **publishes the hashes** to `commitment_hashes_verified.json` before any oracle is opened.

**Why it matters**: Two things to notice in the output:

1. Each commitment is printed with its full 64-hex-character SHA-256 (`sha256: 2d2cca2e…`). Those hashes are written to `commitment_hashes_verified.json` *now*, before the oracle opens; in Step 8 the evaluator re-hashes every commitment and rejects any that no longer matches. That is what makes the commitment tamper-evident.
2. The `restored-004` commitment is `# Unable to determine fix blindly` — the text-only heuristic has no pattern for a disabled control, and solving this task needs the code snippet to be read (Exercise 1.1 adds that). The agent says so instead of guessing. **This is honest failure**, and it's the most pedagogically important line in the demo. Honest systems sometimes fail; dishonest systems always "pass."

**Expected output**:
```
authz-001: if user_id != current_user.id:
    raise AuthorizationError() (sha256: 2d2cca2e3f29d9d15c789539649252c3b550f48a93cf5d10d382a67f0efeb9e9)
depdrift-002: requests==2.31.0 (sha256: 1d277ef3981a3e49b02912a0f03fe1ab563539d7e4e1b5c1e6404a57b19d883f)
poisoned-003: password: 'secure_backup_value' (sha256: bf1b7e3249e23eb25475ef8c42749bedfe57fbd248231e7b03066af19772a9a6)
restored-004: # Unable to determine fix blindly (sha256: 9b08b430f23e23dc55ca8d6d70e0c292a3d13f6ebf945ff9924339d950d9e49a)
Published commitment hashes to commitment_hashes_verified.json
```

---

### Step 7: Verify no leakage in the verified agent

```bash
grep -c "sealed_oracles" demo-01-blind-verification/student/verified_agent.py || echo "0 occurrences — no oracle access"
grep -c "expected_" demo-01-blind-verification/fixtures/scenarios.json || echo "no answer key in the agent's input"
```

**What this does**: Counts references to the oracle file in the verified agent's source, then counts answer-key fields in the one file the agent does read.

**Expected output**:
```
0
0 occurrences — no oracle access
0
no answer key in the agent's input
```
(`grep -c` prints `0` *and* exits non-zero when nothing matches, so the `echo` fires as well.)

**Why it matters**: This is a manual replication of the test `test_leakage_prevention` you'll run in Part 5, which asserts both halves: the source never mentions `sealed_oracles`, and `scenarios.json` contains none of the oracle keys or answer strings. Leakage prevention here is *structural* (the file is never opened, and the file that is opened has nothing to leak), which is stronger than *behavioral* (the agent is told not to look).

---

## ⚖️ Part 4: Open the Oracles and Evaluate

### Step 8: Evaluate both agents against the sealed oracles

```bash
cd demo-01-blind-verification
python3 student/oracle_evaluator.py --commitments commitments_baseline.json --output results/baseline_eval.json
python3 student/oracle_evaluator.py --commitments commitments_verified.json --hashes commitment_hashes_verified.json --output results/verified_eval.json
cd ..
```

**What this does**: This is the **oracle-opening moment**. For each scenario, the evaluator:
1. If a hash ledger was supplied (`--hashes`), re-hashes the submitted commitment and compares it with the hash published in Step 6 — a mismatch is recorded as `commitment_hash_mismatch` and the oracle is never run for that scenario
2. Writes the agent's commitment to a temp file
3. Substitutes the temp path into the oracle's `eval_script`
4. Executes the script via bash with a 10-second timeout
5. Marks PASS if the script's last word of output is PASS, FAIL if it is FAIL, and ERROR (with the last line of stderr) if the script crashed or printed no verdict — for example, a commitment that is not valid Python makes the `authz-001` oracle's `ast.parse` raise `SyntaxError`

**Why it matters**: Notice the sequencing — the evaluator runs *only after* both agents have committed, and for the verified agent the ledger check comes *before* the oracle. The baseline published nothing, so its run says `no hash ledger (unbound commitments)`: its 4/4 is not just leaked, it is also unbound. The three-line sequence above *is* the temporal integrity of the evaluation.

**Expected output**:
```
Evaluation complete: 4/4 passed (no hash ledger (unbound commitments))
  authz-001: PASS
  depdrift-002: PASS
  poisoned-003: PASS
  restored-004: PASS
Evaluation complete: 3/4 passed (hash ledger verified)
  authz-001: PASS
  depdrift-002: PASS
  poisoned-003: PASS
  restored-004: FAIL
```

**See the binding work** (optional, but this is Learning Objective 1 made concrete): open `demo-01-blind-verification/commitments_verified.json`, replace the `restored-004` value with `"return user.mfa_enabled\n"` — the "I would have done X" edit — and re-run the verified evaluation command above. The score stays 3/4 and the edited scenario is reported as:
```
  restored-004: ERROR (commitment_hash_mismatch: commitment was changed after its hash was published)
```
Run the same edited file *without* `--hashes` and it scores 4/4 with no complaint — which is exactly why the ledger exists. Re-run Step 6 to restore the honest commitments before continuing.

---

### Step 9: Interpret the comparison

```bash
cat demo-01-blind-verification/results/baseline_eval.json demo-01-blind-verification/results/verified_eval.json
```

**What this does**: Shows both evaluation results side by side (as two JSON blobs). Each has a per-scenario `results` block, a `hash_ledger_checked` flag (`false` for the baseline, `true` for the verified agent) and a `summary`.

**Why it matters**: Fill in this interpretation table in your lab notes:

| Agent | Score | Read oracle? | Hash-bound? | Meaning |
|-------|-------|--------------|-------------|---------|
| Baseline | 4/4 | ✅ Yes | ❌ No | Measures **oracle leakage**, not capability |
| Verified | 3/4 | ❌ No | ✅ Yes | Measures **genuine blind capability** |

The verified agent's 3/4 is the only trustworthy number. Its single failure (`restored-004`) is *information*: the text-only heuristic has no pattern for a disabled control and would need to read the code. A naive reading ("verified agent is worse!") inverts the lesson.

---

## 🧵 Part 5: Run the Test Suite and Understand Each Test

### Step 10: Run Demo 01's tests

```bash
cd demo-01-blind-verification && python3 -m pytest tests/ -v && cd ..
```

**What this does**: Runs all 18 tests (expected last line: `18 passed`). Group them mentally into five families:

| Test family | Tests | What it proves |
|-------------|-------|----------------|
| **Fixture integrity** | `test_scenarios_exist`, `test_oracles_sealed` | Exactly the four scenarios; every oracle has `oracle_type`, `eval_script`, `expected_commitment` |
| **Agent behavior** | `test_baseline_agent_cheats`, `test_verified_agent_blind`, `test_commitments_are_deterministic` | Baseline scores 4/4; verified publishes a hash for every scenario and scores 3/4 with `restored-004` failing honestly; same input gives the same hashes |
| **Oracle mechanics** | `test_oracle_evaluation`, `test_false_positive_detection`, `test_string_oracle_is_gameable`, `test_false_negative_detection`, `test_oracle_error_is_reported_not_swallowed` | Expected commitments pass; wrong logic fails; a bare `AuthorizationError` token passes (known weakness); formatting sensitivity exists; a crashing oracle is an ERROR with a reason, not a silent FAIL |
| **Commitment binding** | `test_post_hoc_edit_is_detected` | A commitment edited after its hash was published is rejected (`commitment_hash_mismatch`); one with no published hash is rejected too (`commitment_hash_missing`) |
| **Safety & concepts** | `test_leakage_prevention`, `TestComparisonTable::test_generate_comparison`, the five `TestExercises` tests | No oracle in the blind agent's source or input file, no network imports; the comparison table generates with 4/4 vs 3/4; the exercise tests pin the 64-hex hash, the oracle count and the exact-match behavior the exercises rely on |

**Why it matters**: `test_false_negative_detection` deserves special attention. It first submits a *semantically correct* fix with operands reversed (`current_user.id != user_id` instead of `user_id != current_user.id`) — and the containment oracle passes it, because the token `AuthorizationError` is still there. The false negative lives in the *exact-match* output oracle instead: a correct pin with a trailing comment, `requests==2.31.0  # CVE-2024-XXXX`, is rejected. A correct answer failing on formatting is a real weakness of string oracles — production systems use AST-level or semantic comparison. Exercise 1.4 has you explore this.

---

## 🎯 Part 6: Exercises

### Beginner

**Exercise 1.1 — Solve `restored-004` legitimately.**
The blind agent fails `restored-004` because its heuristic only reads the ticket text. Extend `analyze_task` in `verified_agent.py` with a fourth pattern that reads the code in `scenario["codebase"]["files"]`: a function whose body is a constant `return True` under a "temporarily disabled" comment (`require_mfa` in `app/auth/mfa.py`) is a bypassed control, and the fix is `return user.mfa_enabled`. Re-run Steps 6 and 8. The blind score becomes **4/4 (hash ledger verified)** — earned, not copied — and the commitment's hash changes with it. Then run the tests: `test_verified_agent_blind` and `test_generate_comparison` fail because they pin the 3/4 score (and the first also pins the `restored-004` failure); update their expectations to the new, legitimate 4/4.

**What this teaches**: A blind score can rise legitimately, and you can tell *why* it rose. The cheating score was 4/4 from the start and can never tell you anything.

**Exercise 1.1b — Add a fifth scenario.**
Add `crypto-005` to `fixtures/scenarios.json`: a hardcoded API key in `config/settings.py` that must be replaced with an environment-variable lookup — remember, no answer key in this file. Write a matching entry in `sealed_oracles.json` with all three fields: `oracle_type`, `expected_commitment` (the baseline copies this) and an `eval_script` that checks the commitment contains `os.environ` or `getenv`. Run both agents. Record: does the verified agent's heuristic solve it? (Prediction: no — it commits `# Unable to determine fix blindly`; extend `analyze_task` with a `"hardcoded" in text` branch.) Six tests pin the four-scenario set and its 4/4 and 3/4 scores (`SCENARIO_IDS` and the count assertions in `tests/test_blind_verification.py`), so expect them to fail until you update them.

**What this teaches**: Oracle design is a *pair* with task design. A task with no feasible blind solution measures nothing.

### Standard

**Exercise 1.2 — Build a false positive.**
Craft a commitment for `authz-001` that contains the string `AuthorizationError` but does **not** actually prevent unauthorized access (e.g., raise it *after* returning the data). Keep it valid Python, or the oracle's `ast.parse` turns your false positive into an ERROR. Confirm the oracle passes it. Document in your lab notes why string-containment oracles are insufficient.

**What this teaches**: The gap between "contains the right words" and "does the right thing" is exactly the gap adversarial agents will exploit.

**Exercise 1.3 — Seal the oracle for real.**
Modify the workflow: before running the verified agent, compute `sha256(sealed_oracles.json)` and write it to `oracle_seal.txt`. After evaluation, recompute and compare. Then answer: what attack does this *not* prevent? (Hint: it detects oracle *tampering*, not oracle *reading*.)

**What this teaches**: Integrity seals and confidentiality seals are different guarantees. The demo already binds the *commitments* (Step 8's hash ledger); this exercise binds the *oracle*, which matters for more than fairness — `oracle_evaluator.py` runs each `eval_script` with `bash -c`, so a tampered oracle file is arbitrary code execution on the grader. This foreshadows Module 5 (EVIAssure).

### Extension

**Exercise 1.4 — Semantic oracle.**
Replace `authz-001`'s string-containment oracle with a Python AST check: parse the commitment, confirm there is an `if` comparing `user_id` to `current_user.id` (either order) whose body raises `AuthorizationError` *before* any return. Verify your Exercise 1.2 false positive now fails.

**What this teaches**: AST-level oracles shrink the false-positive surface dramatically. This is the same technique you'll use in Module 10's check validator.

---

## 📝 Lab Notes Questions

1. The baseline scored *higher* than the verified agent. In one paragraph, explain to a skeptical manager why the verified agent is the better system.
2. Which oracle (patch vs output) was easier to game? Why?
3. Where exactly does leakage enter this demo's design (which line, in which file), and what — code, tests, or convention — stops the verified agent from taking the same path? What would `test_leakage_prevention` fail to catch?

---

## ✅ Completion Checklist

- [ ] Both agents run; commitments saved, verified agent's hash ledger published
- [ ] Both evaluations run; JSON in `results/`
- [ ] Comparison interpreted (baseline 4/4 = leakage ceiling, unbound; verified 3/4 = real signal, hash-bound)
- [ ] All 18 tests pass
- [ ] At least Beginner exercise complete; Standard strongly recommended
- [ ] `LAB_NOTES.md` Module 1 block filled, including reproducibility fields:
  - [ ] seed `42`, commit (`git rev-parse --short HEAD`), command `make demo DEMO=01`

---

**⬅️ Prev: [Module 0](lab-00-setup.md) | ➡️ Next: [Module 2: Supply Chain & AIBOM](lab-02-supply-chain-aibom.md)**
