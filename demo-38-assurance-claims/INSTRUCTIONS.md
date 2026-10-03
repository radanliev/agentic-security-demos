# Demo 38: Assurance Claims — Execution Instructions

> **Step-by-step guide for students and study participants.**
> For the conceptual background see [README.md](README.md).

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Environment check | 2 min | `python3 --version` |
| Enter demo directory | 1 min | `cd demo-38-assurance-claims` |
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run the demo | 2 min | `python3 student/run_claims.py` |
| Hand-built experiment | 5 min | Flip one flag, re-run, restore |
| Benchmark (full pipeline) | 2 min | `make demo` |
| Record results | 5 min | Fill reproducibility table below |
| **Total** | **~20 min** | |

**Safety**: 100% offline. No network access. All fixtures are synthetic JSON.

---

## Step 0 — Environment Check

From the **repository root** (`agentic-security-demos/`):

```bash
python3 --version          # must be 3.11 or newer
python3 -m pytest --version  # confirms pytest is installed
```

**What this does**: Verifies Python ≥ 3.11 (the demo uses modern type syntax) and that pytest is available.

**Expected**: `Python 3.11.x` (or higher) and `pytest 7.x` (or higher).

**If it fails**: run `make setup` from the repository root, then retry. Without pytest you can still run the demo itself (Step 4), but you cannot complete the tests-FIRST checkpoint (Step 3).

---

## Step 1 — Enter the Demo Directory

```bash
cd demo-38-assurance-claims
```

**What this does**: All remaining commands run from inside this directory so relative paths to `fixtures/` and `student/` resolve.

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

**What this does**: Runs all **19 tests** that verify the demo's correctness: fixture integrity (8 cards, 5 obligations, boolean flags, unique ids), determinism (two subprocess runs agree; the coverage function is pure), coverage tallies (full coverage 2/8 with `third_party` weakest at 2/8, exact per-obligation counts, the card1/card2 full-coverage set, an independent recount, the card3-flip experiment), parity and seed (results file matches memory, exit code 0 with the verbatim table), stdlib-only imports (substring plus AST check), and the results schema (top-level and coverage-block keys, deterministic tie-breaking, edge cases).

**Why tests before demo**: If any test fails, your environment is broken. Fix it now — otherwise you won't know whether a strange demo result is your fault or the code's.

**Expected output (end of run)**:

```
tests/test_assurance_claims.py::TestResultsSchema::test_empty_card_list_yields_zeroes PASSED
====================== 19 passed in 0.XXs ======================
```

✅ **Checkpoint**: You must see `19 passed`. If you see failures, see [Troubleshooting](#troubleshooting) below.

---

## Step 3 — Inspect the Fixture (What You Are About to Code)

```bash
python3 -c "import json; p=json.load(open('fixtures/cards8.json')); print(len(p['cards']), 'cards;', p['obligations']); print([c['id'] for c in p['cards'] if all(c[o] for o in p['obligations'])])"
```

**What this does**: Loads the synthetic card pack without running any evaluation: 8 hand-built card codings over 5 assurance obligations (`threats`, `evals`, `agentic`, `third_party`, `mitigations`).

**Why this step exists**: The tallies you will see in Step 4 are *properties of this file*, chosen by hand — not measurements of real system cards. Reading the input first makes that unmistakable.

**Expected output**:

```
8 cards; ['threats', 'evals', 'agentic', 'third_party', 'mitigations']
['card1', 'card2']
```

Only `card1` and `card2` set every flag — which is why full coverage will be 2/8.

---

## Step 4 — Run the Claims Coding

```bash
python3 student/run_claims.py
```

**What this does**: Codes the eight synthetic system cards against the five assurance obligations (`student/claims.py::coverage` counts, per obligation, how many cards set the flag, plus how many cards cover all five and which obligation is weakest) and writes `results/claims.json`.

**Why this step exists**: This is the *mechanism illustration* — what "coding a public claim against assurance obligations" means operationally: a fixed coding table, deterministic tallies, a weakest-link read-out.

**Expected output** (verbatim):

```
cards 8  obligations 5
obligation    covered
threats       7/8
evals         5/8
agentic       4/8
third_party   2/8
mitigations   7/8
full coverage 2/8
weakest: third_party (2/8).
```

**Files created**: `results/claims.json` (in this directory).

**Interpretation** (record this in your notes):

| Reading | Value | What it means here |
|---------|-------|--------------------|
| Full coverage | 2/8 | Only 2 of 8 cards cover every obligation |
| Weakest obligation | `third_party` at 2/8 | Third-party evaluation is the thinnest public claim — an assurance reader should ask for it first |
| Strongest obligations | `threats`, `mitigations` at 7/8 | Nearly every card says something here |

---

## Step 5 — Hand-Built Experiment (Break It, Then Restore It)

The tallies are hand-picked, so one flag-flip moves them. Try it:

```bash
cp fixtures/cards8.json /tmp/cards8.backup.json
python3 -c "
import json
p = json.load(open('fixtures/cards8.json'))
p['cards'][2]['third_party'] = True   # card3 gains third-party coverage
json.dump(p, open('fixtures/cards8.json', 'w'))
"
python3 student/run_claims.py
python3 -m pytest tests/ -q
```

**What this does**: Gives `card3` third-party coverage, re-runs the demo, and re-runs the tests against your edited fixture.

**Why this step exists**: To show that the verdicts *follow the fixture* — the demo has no model of real cards, only arithmetic over this file. This is the property the research study must earn with real data and a registered protocol.

**Expected output**: the demo now prints `full coverage 3/8` and `weakest: third_party (3/8).` — and the test run **fails** (the hand-picked tallies no longer hold). The failure is the lesson: the tests pin the fixture, so any change to the input is caught.

**Record**: does the weakest link change identity? (No — still `third_party`, now 3/8.) Does full coverage move? (Yes — 2/8 to 3/8.) Why does one card shift both answers? (Because `card3` was already covered on the other four obligations, so gaining the fifth completes it *and* lifts the weakest count.)

**Restore** (required — do not leave the fixture edited):

```bash
cp /tmp/cards8.backup.json fixtures/cards8.json
python3 -m pytest tests/ -q
# Expected: 19 passed
python3 student/run_claims.py
# Expected: the Step 4 table exactly (full coverage 2/8)
```

---

## Step 6 — Benchmark (Full Pipeline via Make)

```bash
make demo
```

**What this does**: Chains setup → the claims run → the printed table (the demo's benchmark: the fixed expected table from Step 4 plus the `results/claims.json` artifact in the standardised result schema).

**Why this step exists**: This is the one-command reproduction of everything above (after the fixture is restored). `make test` re-runs the 19-test suite; `make clean` removes generated files.

**Expected output** (end of run):

```
=== Demo 38: Assurance Claims ===

cards 8  obligations 5
...
weakest: third_party (2/8).

Wrote results/claims.json
```

From the repository root the same pipeline runs as `make demo DEMO=38`.

---

## Step 7 — Inspect and Record Your Results

```bash
cat results/claims.json
```

**Expected content** (`seed` is fixed at 38; `notes` marks the fixture as synthetic):

```json
{
  "demo": "demo-38-assurance-claims",
  "experiment": "assurance-coverage",
  "seed": 38,
  "obligations": ["threats", "evals", "agentic", "third_party", "mitigations"],
  "coverage": {
    "n": 8,
    "per_obligation": {"threats": 7, "evals": 5, "agentic": 4, "third_party": 2, "mitigations": 7},
    "full_coverage": 2,
    "weakest": "third_party",
    "weakest_count": 2
  },
  "notes": "Synthetic teaching fixture"
}
```

---

## Step 8 — Reproducibility Record (Required for Study Participants)

Fill in this table and submit it with your results. Every field is required for your run to be reproducible.

| Field | Your value | How to obtain it |
|-------|------------|------------------|
| Date of run | | today's date |
| Seed | `38` | fixed by the demo |
| Git commit | | `git rev-parse --short HEAD` (from repo root) |
| Python version | | `python3 --version` |
| Operating system | | `uname -a` (macOS/Linux) or `systeminfo` (Windows) |
| Command(s) used | | copy exactly from Steps 2–6 above |
| Tests passed | | `19 passed` (from Step 2) |
| Full coverage | | from Step 4 (expected 2/8) |
| Weakest obligation | | from Step 4 (expected `third_party` at 2/8) |
| Result files | | `results/claims.json` |

**Reproducibility check** (optional but recommended): delete your outputs and re-run Steps 4–7. You must get **identical** tallies and an **identical** `claims.json`. If not, record what differed.

```bash
rm -f results/claims.json
# ...re-run Steps 4 and 6...
diff <(git status --short) <(echo "")   # or simply compare the new claims.json to your saved copy
```

---

## Alternative: One-Command Run

If you want the whole pipeline in one command, from the **repository root**:

```bash
make demo DEMO=38
```

**What this does**: Chains Steps 4–6 automatically (setup → claims coding → printed table) and writes `results/claims.json`.

---

## Exercises (Tiered — see README for full descriptions)

| Level | Exercise | Hint |
|-------|----------|------|
| Beginner | Make `card8` fully covered by setting its four missing flags; predict the new table before re-running | Full coverage becomes 3/8; `evals` and `agentic` each gain one |
| Beginner | Add a sixth obligation (`redteam`) to the fixture and the expected table | Edit `fixtures/cards8.json` + the `EXPECTED_*` constants in the tests; every card starts `false` |
| Standard | Build a **false comfort**: set every flag on a card whose note admits no evidence, and explain why flag-counting cannot catch it | The coder counts flags, not evidence — the research codebook's `present`/`vague` distinction exists for exactly this reason |
| Standard | Write the seeded 10%-style double-code check: code the 8 cards twice (you + a peer) and compute raw agreement | Disagreements cluster on the vaguest obligation — that is what Cohen's kappa would penalize |
| Extension | Replace the boolean flags with the research three-value scheme (`present`/`absent`/`vague` from the paper repo's codebook) and re-derive the table treating `vague` as not covered | Tallies can only stay equal or fall — `vague` never adds coverage |

After any exercise, re-run Step 2 (tests) and Step 4 (evaluation) and record how your changes affected the tallies. Restore the fixture afterwards (`git checkout -- fixtures/`) unless the exercise says otherwise.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'pytest'` | Dependencies not installed | From repo root: `make setup` or `python3 -m pip install pytest` |
| `FileNotFoundError: fixtures/cards8.json` | Wrong working directory | `cd demo-38-assurance-claims` first |
| Tests fail with tallies mismatch (e.g. `assert 3 == 2`) | Fixture edited during Step 5 or exercises | `git checkout -- fixtures/` (or restore from `/tmp/cards8.backup.json`), re-run |
| `19 passed` but demo table differs from Step 4 | You modified student code during exercises | `git checkout -- student/` to restore, re-run |
| `FileNotFoundError: results/claims.json` in a test | Results never written | Run `python3 student/run_claims.py` once, then re-run tests |
| JSON decode error on the fixture | Corrupted fixture (possibly hand-edited) | `git checkout -- fixtures/` to restore |
| Windows: `make` not found | No make | Run the underlying commands directly (`python3 student/run_claims.py`, `python3 -m pytest tests/`), or use WSL |
| `python: command not found` | System lacks `python` alias | Use `python3` everywhere (this demo never calls bare `python`) |

---

## Safety Reminder

⚠️ **Teaching demonstration using synthetic fixtures only.** No real system cards, vendors, credentials, or network access. Results demonstrate a mechanism; they are not evidence about real cards. See [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md).
