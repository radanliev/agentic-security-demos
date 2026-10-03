# Demo 39: Incident Taxonomy — Execution Instructions

> **Step-by-step guide for students and study participants.**
> For the conceptual background see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 2 min | `python3 --version` |
| Enter demo directory | 1 min | `cd demo-39-incident-taxonomy` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 2 min | `python3 student/run_tax.py` |
| Inspect results | 1 min | `cat results/taxonomy.json` |
| Hand-built experiment | 3 min | Edit one fixture row, re-run |
| Benchmark comparison | 2 min | Restore fixture, compare with reference |
| Record results | 5 min | Fill reproducibility table below |
| **Total** | **~15 min** | |

**Safety**: 100% offline. No network access. All fixtures are synthetic JSON.

---

## Step 0 — Environment Check

From the **repository root**:

```bash
python3 --version          # must be 3.11 or newer
python3 -m pytest --version  # confirms pytest is installed
```

**What this does**: Verifies Python ≥ 3.11 (the demo uses modern type syntax) and that pytest is available.

**Expected**: `Python 3.11.x` (or higher) and `pytest 7.x` (or higher).

**If it fails**: run `make setup` from the repository root, then retry.

---

## Step 1 — Enter the Demo Directory

```bash
cd demo-39-incident-taxonomy
```

**What this does**: All remaining commands run from inside this directory so relative paths to `fixtures/` and `student/` resolve.

**Verify you are in the right place**:

```bash
ls
# Expected: CITATION.cff  INSTRUCTIONS.md  Makefile  README.md  fixtures  results  student  tests
```

**Why this step exists**: Every path below (`fixtures/incidents.json`, `student/run_tax.py`, `results/taxonomy.json`) is relative. Running from anywhere else produces `FileNotFoundError`, which looks like broken code but is only a wrong directory.

---

## Step 2 — Run the Tests FIRST (Baseline Sanity Check)

```bash
python3 -m pytest tests/ -v
```

**What this does**: Runs all **19 tests** that verify the demo's correctness: fixture integrity (10 incidents with unique ids, schema of sketches and controls, seed 39), determinism (identical stdout and byte-identical results across runs), the hand-built pattern counts (prompt-injection 4, tool-misuse 3, data-exfiltration 2, privilege-escalation 1), the control catalogue (7/10 supported, exact supported ids), seed parity between fixture and results, the exact stdout lines, stdlib-only imports, and the results-file schema.

**Why tests before demo**: If any test fails, your environment or fixture is broken. Fix it now — otherwise you won't know whether a strange demo result is your fault or the code's.

**Expected output (end of run)**:

```
tests/test_incident_taxonomy.py::test_results_schema PASSED
============================== 19 passed in 0.XXs ==============================
```

✅ **Checkpoint**: You must see `19 passed`. If you see failures, see [Troubleshooting](#troubleshooting) below.

---

## Step 3 — Run the Tally

```bash
python3 student/run_tax.py
```

**What this does**: Tallies the 10 synthetic incident sketches in `fixtures/incidents.json` into attack patterns with `student/taxonomy.py:top_pattern`, scores the static 10-item control catalogue with `supported_controls`, writes `results/taxonomy.json`, and prints the summary table.

**Why this step exists**: This is the demo's *mechanism* — turning incident reports into counts (which pattern recurs) and checking which controls already cover them. The numbers are properties of the hand-built fixture, not field measurements.

**Expected output** (verbatim):

```text
incidents 10  controls 10
pattern               count
data-exfiltration     2/10
privilege-escalation  1/10
prompt-injection      4/10
tool-misuse           3/10
top pattern: prompt-injection (4/10)
supported controls: 7/10.
```

**Files created**: `results/taxonomy.json`.

---

## Step 4 — Inspect the Results File

```bash
cat results/taxonomy.json
```

**What this does**: Shows the machine-readable artefact the tally wrote — the same dict `main()` returned, in the standard result schema (`demo`, `experiment`, `seed`, `top_pattern`, `controls`, `notes`).

**Why this step exists**: Downstream analysis never reads stdout; it reads this file. Checking its schema now is what `test_results_schema` automates.

**Expected content** (`top_pattern.counts` preserves the 4/3/2/1 split; `controls.supported_ids` lists exactly `ctl01`–`ctl07`):

```json
{
  "demo": "demo-39-incident-taxonomy",
  "experiment": "incident-tally",
  "seed": 39,
  "top_pattern": {
    "pattern": "prompt-injection",
    "count": 4,
    "n": 10,
    "counts": {
      "prompt-injection": 4,
      "tool-misuse": 3,
      "data-exfiltration": 2,
      "privilege-escalation": 1
    }
  },
  "controls": {
    "n": 10,
    "supported": 7,
    "supported_ids": [
      "ctl01",
      "ctl02",
      "ctl03",
      "ctl04",
      "ctl05",
      "ctl06",
      "ctl07"
    ]
  },
  "notes": "Synthetic teaching fixture"
}
```

**Save a reference copy** — you will benchmark against it in Step 6:

```bash
cp results/taxonomy.json /tmp/taxonomy_reference.json
```

---

## Step 5 — Hand-Built Experiment: Break the Tally

Change `inc10`'s pattern from `privilege-escalation` to `tool-misuse` in `fixtures/incidents.json`, then re-run both commands:

```bash
python3 student/run_tax.py
python3 -m pytest tests/ -q
```

**What this does**: Moves one sketch across patterns, so tool-misuse rises to 4/10 and ties prompt-injection at the top, while privilege-escalation drops out of the table entirely.

**Why this step exists**: This is the *experiment*. Real taxonomies wobble when one report is recoded; here you cause the wobble on purpose and watch what breaks — the table, the top-pattern verdict, and the tests.

**Expected output** (verbatim — note the tie and the vanished row):

```text
incidents 10  controls 10
pattern               count
data-exfiltration     2/10
prompt-injection      4/10
tool-misuse           4/10
top pattern: prompt-injection (4/10)
supported controls: 7/10.
```

**Expected test result**: failures — `test_each_pattern_count`, `test_top_pattern_is_prompt_injection` and `test_pattern_counts_sum_to_ten` no longer hold, because you changed the fixture the tests pin. That is the tests doing their job: the counts are *fixture properties*, and the suite reports exactly which property moved.

⚠️ **Important observation**: the top pattern stays `prompt-injection` despite the 4/4 tie. The tie-break is deterministic (alphabetically-first maximum) and pinned by `test_tie_break_is_deterministic`. Record this in your notes: practitioner guidance must state its tie-break rule, because counts alone do not settle a tie.

---

## Step 6 — Benchmark: Restore and Compare Against the Reference

Restore the pristine fixture and confirm the benchmark (reference) output returns byte-identically:

```bash
git checkout -- fixtures/
python3 student/run_tax.py
diff /tmp/taxonomy_reference.json results/taxonomy.json && echo "benchmark matches"
python3 -m pytest tests/ -q
```

**What this does**: `git checkout` undoes your Step-5 edit; the re-run regenerates the results; `diff` compares them against the reference copy saved in Step 4; the test run confirms all 19 pass again.

**Why this step exists**: This is the *benchmark comparison* — perturbed run (Step 5) versus reference run (Step 4). In the research study this role is played by the frozen corpus: every later coding pass is diffed against the frozen reference, and any silent change is a breach. Here the reference is your saved JSON.

**Expected output** (verbatim):

```text
benchmark matches
19 passed in 0.XXs
```

**Interpretation** (record this in your notes):

| Run | Top pattern | Supported controls | What it measures |
|-----|-------------|--------------------|------------------|
| Reference (Steps 3–4) | prompt-injection 4/10 | 7/10 | The hand-built fixture, pinned by 19 tests |
| Perturbed (Step 5) | prompt-injection 4/10 (tie) | 7/10 | Sensitivity to one recoded sketch |
| Restored (this step) | prompt-injection 4/10 | 7/10 | Reproducibility: identical bytes |

---

## Step 7 — Reproducibility Record (Required for Study Participants)

Fill in this table and submit it with your results. Every field is required for your run to be reproducible.

| Field | Your value | How to obtain it |
|-------|------------|------------------|
| Date of run | | today's date |
| Seed | `39` | fixed by the demo |
| Git commit | | `git rev-parse --short HEAD` (from repo root) |
| Python version | | `python3 --version` |
| Operating system | | `uname -a` (macOS/Linux) or `systeminfo` (Windows) |
| Command(s) used | | copy exactly from Steps 2–6 above |
| Tests passed | | `19 passed` (from Step 2) |
| Top pattern | | from Step 3 (expected prompt-injection 4/10) |
| Supported controls | | from Step 3 (expected 7/10) |
| Reference file | | `/tmp/taxonomy_reference.json` vs `results/taxonomy.json` |
| Result files | | `results/taxonomy.json` |

**Reproducibility check** (optional but recommended): delete your outputs and re-run Steps 3–4. You must get **identical** bytes. If not, record what differed.

```bash
rm -f results/taxonomy.json
python3 student/run_tax.py
diff /tmp/taxonomy_reference.json results/taxonomy.json && echo "reproduced"
```

**Expected**: `reproduced`.

---

## Alternative: One-Command Run

If you want the whole pipeline in one command, from the **repository root**:

```bash
make demo DEMO=39
```

**What this does**: Chains setup → tally (`student/run_tax.py`) automatically and prints the final JSON.

**Expected**: the same tally table as Step 3, followed by the contents of `results/taxonomy.json`.

---

## Exercises (Tiered — see README for full descriptions)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Recode `inc05` from `tool-misuse` to `data-exfiltration` and predict the new table *before* running | Counts become 4/2/3/1; top stays prompt-injection; two tests fail — which ones, and why those? |
| Beginner | Add an eleventh sketch `inc11` with a brand-new pattern `model-exfiltration` | The counts dict gains a fifth key; `test_fixture_has_ten_incidents_with_unique_ids` fails by design — update fixture *and* tests together, never silently |
| Standard | Add an eleventh control `ctl11` (unsupported, e.g. "Formal policy verification v2") and recompute support | Support drops to 7/11; which tests pin the denominator, and what does a bare "7 supported" hide without it? |
| Standard | Force a three-way tie (4/4/2 → move one sketch so three patterns sit at 3/10) and document the winner | The alphabetical tie-break picks the verdict; write the one-line tie-break rule the guidance would need |
| Extension | Wire each pattern to the controls that cover it (a `covers` list per control) and report coverage per pattern | Which pattern, if any, has zero covering controls — and why does that question need a mapping the fixture does not ship? |

After any exercise, re-run Step 2 (tests) and Step 3 (tally) and record how your changes affected the scores. Restore with `git checkout -- fixtures/` when done.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'pytest'` | Dependencies not installed | From repo root: `make setup` or `python3 -m pip install -r requirements.txt` |
| `FileNotFoundError: fixtures/incidents.json` | Wrong working directory | `cd demo-39-incident-taxonomy` first |
| `python3: command not found` | No Python 3 on PATH | Install Python 3.11+; `which python3` to check |
| Tests fail right after Step 5 edits | You changed the fixture (expected) | That is the experiment working; `git checkout -- fixtures/` restores, re-run for 19 passed |
| `19 passed` but tally differs from Step 3 | You modified fixtures or student code during exercises | `git checkout -- fixtures/ student/` to restore, re-run |
| Tie confusion: top unchanged at 4/4 | Deterministic alphabetical tie-break | See Step 5 observation and `test_tie_break_is_deterministic` |
| `diff` reports a difference after restore | Stale reference or un-restored edit | Re-save the reference from a clean run, or `git status --short` to find the edit |
| Windows: `make` not found | No make | Run the underlying commands directly (`python3 student/...`), or use WSL |
| `results/taxonomy.json` missing after clean | `make clean` removed `results/` | `make setup` recreates it, or just re-run `python3 student/run_tax.py` |

---

## Safety Reminder

⚠️ **Teaching demonstration using synthetic fixtures only.** No real incidents, victims, credentials, or network access. Results demonstrate a counting mechanism; they are not evidence about real incidents. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
