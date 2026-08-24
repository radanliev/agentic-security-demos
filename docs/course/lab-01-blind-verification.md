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

**Why it matters**: These are the *only* inputs the honest (verified) agent ever sees. Notice each scenario has `task`, `context`, `codebase.files` — but the `hidden_oracle` block is *also* in this file. That's deliberate: the demo's honesty boundary is enforced by **code discipline** (the verified agent simply never reads that block), not by cryptography. Module 1's exercises ask you to critique this and sketch a stronger seal.

**What to look for**: In `authz-001`, the vulnerable code is:
```python
def get_user_data(user_id, current_user):
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
- `commitment_hash` — in the real research benchmark this binds the agent to its commitment cryptographically; here it's a placeholder
- `eval_script` — a shell command that writes PASS or FAIL given a commitment file

Look at `authz-001`'s eval script: it checks whether the string `AuthorizationError` appears in the commitment. Simple? Yes. Gameable? Also yes — a commitment containing the word but not the logic would pass. That's a **false positive**, and Exercise 2 (standard) has you build one.

---

## 🧪 Part 2: Run the Cheating Baseline

### Step 3: Run the baseline agent

```bash
cd demo-01-blind-verification
python3 student/baseline_agent.py
```

*(Return to repo root afterward: `cd ../..` — or run the remaining commands from root as shown.)*

**What this does**: Runs `student/baseline_agent.py`, which loads **both** `scenarios.json` **and** `sealed_oracles.json`, extracts the expected answer from each eval script, and writes it out as its "commitment." It saves results to `commitments_baseline.json`.

**Why it matters**: The baseline is not stupid — it's *dishonest by construction*. It demonstrates the upper bound of what's achievable when the oracle leaks. Its 4/4 score is the "teaching to the test" ceiling.

**Expected output**:
```
authz-001: +    if user_id != current_user.id: ...
depdrift-002: requests==2.31.0
poisoned-003: password: 'secure_backup_value'
restored-004: return user.mfa_enabled
```

### Step 4: Confirm the baseline read the oracle

```bash
grep -n "sealed_oracles" demo-01-blind-verification/student/baseline_agent.py
```

**What this does**: Searches the baseline source for the oracle-loading line.

**Why it matters**: You should find `self.oracles = json.loads(oracles_path.read_text())["sealed_oracles"]`. This single line is the entire vulnerability. When we later check the verified agent (Step 7), that line will be absent — provenance of behavior, enforced by inspection.

---

## 🛡️ Part 3: Run the Honest Blind Agent

### Step 5: Inspect the verified agent's inputs

```bash
grep -n "Path(" demo-01-blind-verification/student/verified_agent.py | head -5
```

**What this does**: Shows which files the verified agent opens.

**Why it matters**: You will see it opens **only** `fixtures/scenarios.json`. It never constructs a path to `sealed_oracles.json`. This is the operational definition of *blind* in this demo: **the agent's input surface contains no oracle**.

---

### Step 6: Run the verified agent

```bash
cd demo-01-blind-verification && python3 student/verified_agent.py && cd ../..
```

**What this does**: Runs the honest agent. It reads each scenario's `task` and `context`, applies simple keyword heuristics ("authorization" → emit the authz check; "cve" → bump the dependency; "backup" → restore from `.bak`; "mfa" → return the real flag), computes a SHA-256 **commitment hash** of its answer, and writes `commitments_verified.json`.

**Why it matters**: Two things to notice in the output:

1. Each commitment is printed with a hash like `2d2cca2e3f29d9d1` — that's the first 16 hex chars of SHA-256 of the commitment text. In a real system, the agent would *publish* this hash before the oracle opens, making the commitment tamper-evident.
2. The `restored-004` commitment is `# Unable to determine fix blindly` — the heuristic genuinely couldn't solve it without more context. **This is honest failure**, and it's the most pedagogically important line in the demo. Honest systems sometimes fail; dishonest systems always "pass."

**Expected output**:
```
authz-001: if user_id != current_user.id:
    raise AuthorizationError() (hash: 2d2cca2e3f29d9d1)
depdrift-002: requests==2.31.0 (hash: 1d277ef3981a3e49)
poisoned-003: password: 'secure_backup_value' (hash: bf1b7e3249e23eb2)
restored-004: # Unable to determine fix blindly (hash: 9b08b430f23e23dc)
```

---

### Step 7: Verify no leakage in the verified agent

```bash
grep -c "sealed_oracles" demo-01-blind-verification/student/verified_agent.py || echo "0 occurrences — no oracle access"
```

**What this does**: Counts references to the oracle file in the verified agent's source.

**Why it matters**: Output should be `0 occurrences`. This is a manual replication of the test `test_leakage_prevention` you'll run in Part 5. Leakage prevention here is *structural* (the file is never opened), which is stronger than *behavioral* (the agent is told not to look).

---

## ⚖️ Part 4: Open the Oracles and Evaluate

### Step 8: Evaluate both agents against the sealed oracles

```bash
cd demo-01-blind-verification
python3 student/oracle_evaluator.py --commitments commitments_baseline.json --output results/baseline_eval.json
python3 student/oracle_evaluator.py --commitments commitments_verified.json --output results/verified_eval.json
cd ../..
```

**What this does**: This is the **oracle-opening moment**. For each scenario, the evaluator:
1. Writes the agent's commitment to a temp file
2. Substitutes the temp path into the oracle's `eval_script`
3. Executes the script via bash with a 10-second timeout
4. Marks PASS if the script printed PASS

**Why it matters**: Notice the sequencing — the evaluator runs *only after* both agents have committed. In the real research benchmark, the commitment hash would be checked against the submitted commitment first, rejecting any post-hoc edits. The two-line sequence above *is* the temporal integrity of the evaluation.

**Expected output**:
```
Evaluation complete: 4/4 passed
  authz-001: PASS
  depdrift-002: PASS
  poisoned-003: PASS
  restored-004: PASS
Evaluation complete: 3/4 passed
  authz-001: PASS
  depdrift-002: PASS
  poisoned-003: PASS
  restored-004: FAIL
```

---

### Step 9: Interpret the comparison

```bash
cat demo-01-blind-verification/results/baseline_eval.json demo-01-blind-verification/results/verified_eval.json
```

**What this does**: Shows both evaluation results side by side (as two JSON blobs).

**Why it matters**: Fill in this interpretation table in your lab notes:

| Agent | Score | Read oracle? | Meaning |
|-------|-------|--------------|---------|
| Baseline | 4/4 | ✅ Yes | Measures **oracle leakage**, not capability |
| Verified | 3/4 | ❌ No | Measures **genuine blind capability** |

The verified agent's 3/4 is the only trustworthy number. Its single failure (`restored-004`) is *information*: the heuristic needs more context for control-restoration tasks. A naive reading ("verified agent is worse!") inverts the lesson.

---

## 🧵 Part 5: Run the Test Suite and Understand Each Test

### Step 10: Run Demo 01's tests

```bash
cd demo-01-blind-verification && python3 -m pytest tests/ -v && cd ../..
```

**What this does**: Runs all 15 tests. Group them mentally into four families:

| Test family | Tests | What it proves |
|-------------|-------|----------------|
| **Fixture integrity** | `test_scenarios_exist`, `test_oracles_sealed` | Fixtures well-formed, oracles have required fields |
| **Agent behavior** | `test_baseline_agent_cheats`, `test_verified_agent_blind` | Baseline produces 4 commitments; verified produces 4 without oracle access |
| **Oracle mechanics** | `test_oracle_evaluation`, `test_false_positive_detection`, `test_false_negative_detection` | Correct commitments pass; wrong logic fails; formatting sensitivity exists |
| **Safety & concepts** | `test_leakage_prevention`, `test_post_hoc_explanation_insufficient`, comparison table | No oracle access; post-hoc unverifiable; table generates |

**Why it matters**: `test_false_negative_detection` deserves special attention. It submits a *semantically correct* fix with operands reversed (`current_user.id != user_id` instead of `user_id != current_user.id`). The strict string-matching oracle may reject it. This is a real weakness of string/regex oracles — production systems use AST-level or semantic comparison. Exercise 4 has you explore this.

---

## 🎯 Part 6: Exercises

### Beginner

**Exercise 1.1 — Add a fifth scenario.**
Add `crypto-005` to `fixtures/scenarios.json`: a hardcoded API key in `config/settings.py` that must be replaced with an environment-variable lookup. Write a matching oracle in `sealed_oracles.json` that checks the commitment contains `os.environ` or `getenv`. Run both agents. Record: does the verified agent's heuristic solve it? (Prediction: no — extend `analyze_task` in `verified_agent.py` with a `"hardcoded" in task` branch.)

**What this teaches**: Oracle design is a *pair* with task design. A task with no feasible blind solution measures nothing.

### Standard

**Exercise 1.2 — Build a false positive.**
Craft a commitment for `authz-001` that contains the string `AuthorizationError` but does **not** actually prevent unauthorized access (e.g., raise it *after* returning the data). Confirm the oracle passes it. Document in your lab notes why string-containment oracles are insufficient.

**What this teaches**: The gap between "contains the right words" and "does the right thing" is exactly the gap adversarial agents will exploit.

**Exercise 1.3 — Seal the oracle for real.**
Modify the workflow: before running the verified agent, compute `sha256(sealed_oracles.json)` and write it to `oracle_seal.txt`. After evaluation, recompute and compare. Then answer: what attack does this *not* prevent? (Hint: it detects oracle *tampering*, not oracle *reading*.)

**What this teaches**: Integrity seals and confidentiality seals are different guarantees. This foreshadows Module 5 (EVIAssure).

### Extension

**Exercise 1.4 — Semantic oracle.**
Replace `authz-001`'s string-containment oracle with a Python AST check: parse the commitment, confirm there is an `if` comparing `user_id` to `current_user.id` (either order) whose body raises `AuthorizationError` *before* any return. Verify your Exercise 1.2 false positive now fails.

**What this teaches**: AST-level oracles shrink the false-positive surface dramatically. This is the same technique you'll use in Module 10's check validator.

---

## 📝 Lab Notes Questions

1. The baseline scored *higher* than the verified agent. In one paragraph, explain to a skeptical manager why the verified agent is the better system.
2. Which oracle (patch vs output) was easier to game? Why?
3. Where exactly does leakage enter this demo's design, and what single code change would most reduce it?

---

## ✅ Completion Checklist

- [ ] Both agents run; commitments saved
- [ ] Both evaluations run; JSON in `results/`
- [ ] Comparison interpreted (baseline 4/4 = leakage ceiling; verified 3/4 = real signal)
- [ ] All 15 tests pass
- [ ] At least Beginner exercise complete; Standard strongly recommended
- [ ] `LAB_NOTES.md` Module 1 block filled, including reproducibility fields:
  - [ ] seed `42`, commit (`git rev-parse --short HEAD`), command `make demo DEMO=01`

---

**⬅️ Prev: [Module 0](lab-00-setup.md) | ➡️ Next: [Module 2: Supply Chain & AIBOM](lab-02-supply-chain-aibom.md)**
