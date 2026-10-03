# Demo 31: Integration Scope Creep — Execution Instructions

> **Step-by-step guide for students and study participants.**
> For the conceptual background see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 2 min | `python3 --version` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 2 min | `python3 student/run_scopes.py` |
| Break-it experiment | 5 min | Edit `fixtures/integrations.json`, re-run |
| Record results | 5 min | Fill reproducibility table below |
| **Total** | **~15 min** | |

**Safety**: 100% offline. No network access. All fixtures are synthetic JSON.

---

## Step 0 — Environment Check

From the **repository root** (`agentic-security-demos/`):

```bash
python3 --version          # must be 3.11 or newer
python3 -m pytest --version  # confirms pytest is installed
```

**What this does**: Verifies Python ≥ 3.11 (the demo uses `sys.stdlib_module_names`
in its stdlib-only test) and that pytest is available.

**Expected**: `Python 3.11.x` (or higher) and `pytest 7.x` (or higher).

**If it fails**: install Python 3.11+ and `pip install pytest`, then retry.

---

## Step 1 — Enter the Demo Directory

```bash
cd demo-31-scope-creep
```

**What this does**: All remaining commands run from inside this directory so
relative paths to `fixtures/` and `student/` resolve.

**Verify you are in the right place**:

```bash
ls
# Expected: CITATION.cff  INSTRUCTIONS.md  Makefile  README.md  fixtures  results  student  tests
```

---

## Step 2 — Run the Tests FIRST (Baseline Sanity Check)

```bash
python3 -m pytest tests/ -v
```

**What this does**: Runs all **21 tests** that verify the demo's correctness:
fixture integrity (eight hand-built integrations, unique ids `i1`–`i8`, seed 31,
every row with `requested`/`used` lists), determinism (two runs print identical
output, table matches the hand-built expectation), over-privilege verdicts
(5/8 over-privileged with exact ids, tight ids, the `i1` admin-creep and `i8`
`drive.admin` cases), the least-privilege union rule (sorted union of used
scopes, 8 scopes), the strict-superset rule (equal is tight, strict superset is
over, empty edge cases), results parity (disk equals memory, seed 31, schema
keys, partition of all eight ids), and the stdlib-only import check.

**Why tests before demo**: If any test fails, your environment is broken. Fix it
now — otherwise you won't know whether a strange demo result is your fault or
the code's.

**Expected output (end of run)**:

```
tests/test_scopes.py::test_student_code_is_stdlib_only PASSED
============================== 21 passed in 0.XXs ==============================
```

✅ **Checkpoint**: You must see `21 passed`. If you see failures, see
[Troubleshooting](#troubleshooting) below.

---

## Step 3 — Run the Scope Check (The Hand-Built Experiment)

```bash
python3 student/run_scopes.py
```

**What this does**: Evaluates eight hand-built integrations with the
strict-superset rule (`set(requested) > set(used)` means over-privileged) and
computes the least-privilege set as the sorted union of all used scopes. Writes
`results/scopes.json`.

**Why this step exists**: This is the *measurement*. Each integration declares
what it requests and what it uses; the gap between the two is scope creep, and
the union of used scopes is the policy that would grant nothing unused.

**Expected output**:

```
id   over  requested>used
i1   True   3>1
i2   False  1>1
i3   False  2>2
i4   True   3>1
i5   True   2>1
i6   True   2>1
i7   False  1>1
i8   True   3>2
over-privileged 5/8  least-privilege 8 scopes
least: calendar.read,chat,drive.read,drive.write,files.read,read,repo,write
```

**Files created**: `results/scopes.json` (in this directory).

---

## Step 4 — Inspect the Results File (The Benchmark Record)

```bash
cat results/scopes.json
```

**What this does**: Shows the demo's final artifact in the standardized result
schema: demo name, experiment, seed, totals, verdict ids, least-privilege set,
per-row verdicts, and the synthetic-fixture note.

**Expected content** (`rows` abbreviated here; the file holds all eight):

```json
{
  "demo": "demo-31-scope-creep",
  "experiment": "scope-creep",
  "seed": 31,
  "total": 8,
  "overprivileged": 5,
  "overprivileged_ids": ["i1", "i4", "i5", "i6", "i8"],
  "least_privilege": ["calendar.read", "chat", "drive.read", "drive.write", "files.read", "read", "repo", "write"],
  "notes": "Synthetic teaching fixture"
}
```

**Interpretation** (record this in your notes):

| Group | Score | Members | What it means |
|-------|-------|---------|---------------|
| Over-privileged | 5/8 | i1, i4, i5, i6, i8 | Request strictly more than they use |
| Tight | 3/8 | i2, i3, i7 | Request exactly what they use |
| Least-privilege | 8 scopes | union of all used | Policy granting nothing unused |

---

## Step 5 — Break It (Hand-Built Experiment)

Add `admin` to the `used` list of `i1` in `fixtures/integrations.json` and
re-run both commands:

```bash
python3 -m pytest tests/ -q
python3 student/run_scopes.py
```

**What this does**: Tests whether using more scopes fixes creep. `i1` requested
`read`, `write`, `admin` and now uses `read`, `admin` — but `write` is still
requested and unused, so `i1` stays over-privileged.

**Expected**: `i1` is still over-privileged (`True`, now `3>2`); the
least-privilege union gains `admin` (9 scopes); at least two tests fail (the
5/8 count and the union expectation), which is the suite correctly detecting
your edit.

**Why this matters**: Using more does not fix creep — only requesting less
does. That asymmetry is the least-privilege lesson.

Restore the fixture when done:

```bash
git checkout -- fixtures/
python3 -m pytest tests/ -q
# Expected: 21 passed
```

---

## Step 6 — Reproducibility Record (Required for Study Participants)

Fill in this table and submit it with your results. Every field is required for
your run to be reproducible.

| Field | Your value | How to obtain it |
|-------|------------|------------------|
| Date of run | | today's date |
| Seed | `31` | fixed by the demo |
| Git commit | | `git rev-parse --short HEAD` (from repo root) |
| Python version | | `python3 --version` |
| Operating system | | `uname -a` (macOS/Linux) or `systeminfo` (Windows) |
| Command(s) used | | copy exactly from Steps 3–4 above |
| Tests passed | | `21 passed` (from Step 2) |
| Over-privileged | | from Step 3 (expected 5/8) |
| Least-privilege scopes | | from Step 3 (expected 8 scopes) |
| Result files | | `results/scopes.json` |

**Reproducibility check** (optional but recommended): delete your outputs and
re-run Steps 3–4. You must get **identical** verdicts and an **identical**
results file. If not, record what differed.

```bash
rm -f results/scopes.json
python3 student/run_scopes.py
# ...compare the new results/scopes.json to your saved copy...
```

---

## Alternative: One-Command Run

If you want the whole pipeline in one command, from the **repository root**:

```bash
make demo DEMO=31
```

**What this does**: Chains setup → the scope-check run automatically
(`setup` verifies Python and creates `results/`, then `student/run_scopes.py`)
and prints the final table.

---

## Exercises (Tiered — see README for the learning objectives)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Make `i5` tight without changing what it uses | Remove `files.write` from its `requested` list; the count becomes 4/8 and `test_five_of_eight_overprivileged` must be updated to expect it |
| Beginner | Add a ninth integration (`i9`) that is tight | Append `{"id": "i9", "provider": "chat", "requested": ["chat"], "used": ["chat"]}` to `fixtures/integrations.json`; update the total/id tests |
| Standard | Build a **near miss**: an integration that requests *fewer* scopes than it uses | The strict-superset rule calls it tight — explain why under-requesting is a different failure mode (breakage, not creep) |
| Standard | Compute per-provider creep rates from the fixture | Group `i1`–`i8` by `provider`; which provider has the highest over-privilege fraction, and why is n=8 too small to generalize? |
| Extension | Replace the strict-superset rule with a severity score | Score each integration by `len(requested - used)` weighted by a sensitivity map (e.g. `admin` > `write` > `read`); re-rank `i1`–`i8` and defend the weights |

After any exercise, re-run Step 2 (tests) and Step 3 (evaluation) and record how
your changes affected the verdicts.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'pytest'` | Dependencies not installed | `python3 -m pip install pytest`, then retry |
| `FileNotFoundError: fixtures/integrations.json` | Wrong working directory | `cd demo-31-scope-creep` first |
| `AssertionError` in `test_student_code_is_stdlib_only` | A non-stdlib import was added to `student/` | Remove the import; the demo is offline by design |
| Tests fail with JSON decode error | Corrupted fixture (possibly edited) | `git checkout -- fixtures/` to restore |
| `21 passed` but demo output differs from expected | You modified student code during exercises | `git checkout -- student/ fixtures/` to restore, re-run |
| `least` line shows 9 scopes including `admin` | Step 5 edit is still in place | `git checkout -- fixtures/`, re-run Steps 2–3 |
| Windows: `make` not found | No make | Run the underlying commands directly (`python3 student/...`), or use WSL |

---

## Safety Reminder

⚠️ **Teaching demonstration using synthetic fixtures only.** No real providers,
tokens, or credentials. No network access (standard library only). Results
demonstrate a mechanism; they are not evidence about real integrations. See
[RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
