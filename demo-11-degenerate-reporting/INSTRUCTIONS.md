# Demo 11: Degenerate Reporting — Execution Instructions

> **Step-by-step guide for students and study participants.**
> Concepts: [README.md](README.md)

---

## ⏱️ Overview

| What | Time | Command |
|------|------|---------|
| Run tests | 1 min | `python3 -m pytest tests/ -v` |
| Run both reviewers | 1 min | `python3 student/audit_reporting.py` |
| Rescore Case Study Zero | 2 min | inline script (Step 5) |
| Generate results | 1 min | `python3 student/generate_audit_results.py` |
| Exercises 11.1–11.3 | 10 min | pen, paper, terminal |
| **Total** | **~15 min** | |

**Safety:** 100% offline. **No real papers, no network, no credentials** — only invented JSON records. Verify: `grep -R "requests\|urllib\|socket" student/` returns nothing, and `test_demo_runs_with_execution_disabled` runs the whole demo with `exec`/`eval` poisoned.

---

## Step 0 — Enter the Demo Directory

From the **repository root**:

```bash
cd demo-11-degenerate-reporting
```

**Verify:**

```bash
ls
# Expected: Makefile  README.md  INSTRUCTIONS.md  fixtures  results  student  tests
```

All remaining commands use relative paths (`fixtures/papers.json`), so you must be inside this directory.

---

## Step 1 — Read the Fixtures and Predict

```bash
cat fixtures/papers.json | python3 -c "import json,sys; [print(p['id'], '| n=%d' % p['n_trials'], '| baselines=%s' % p['baselines_reported'], '| ASR-after=%s' % p.get('asr_after')) for p in json.load(sys.stdin)['papers']]"
```

**What this does:** Prints one line per synthetic paper: sample size, reported baselines, reported post-defence attack rate.

**Why it matters:** Before running, fill this prediction table — which papers will the *naive reviewer* accept, and which will the *auditor* pass?

| ID | ASR-after | Baselines | Naive will… | Auditor will… |
|----|-----------|-----------|-------------|---------------|
| `P-01` | 0.02 | always-allow, random | ? | ? |
| `P-02` | 0.03 | (none) | ? | ? |
| `P-03` | 0.04 | no-defence | ? | ? |
| `P-04` | — (acc 0.97) | majority-class (no score) | ? | ? |
| `P-05` | 0.00 | always-allow | ? | ? |
| `P-06` | 0.00 | always-allow, always-block, majority-class | ? | ? |
| `P-07` | 0.05 | always-allow, random (n=20) | ? | ? |
| `P-08` | 0.06 | always-allow, random (no counts) | ? | ? |

**Also read the case file** (`fixtures/case_zero.json`): 12 sealed labels, verdicts from policies E and F. Predict: under a scorer that marks "correct" whenever the policy says MALICIOUS, who wins — and would the sealed labels agree?

---

## Step 2 — Run the Tests

```bash
python3 -m pytest tests/ -v
```

**Expected:** `23 passed`. The suite checks the answer key (P-01/P-06 PASS; P-02–P-05 FAIL; P-07/P-08 INCONCLUSIVE), the Case Zero inversion (reported E 8/12 > F 4/12; rescored F 11/12 > E 9/12), offline execution, determinism, and anonymity (no real identities, keys, or paths anywhere in the demo).

**If a test fails:** stop — do not continue to Step 3. Record the failure; a red suite means the fixture or the auditor changed, and every number downstream is suspect.

---

## Step 3 — Run Both Reviewers

```bash
python3 student/audit_reporting.py
```

**Expected output (exact):**

```
Paper Naive    Audit         Reason (first failing check)
------------------------------------------------------------------------------
P-01  ACCEPT   PASS          all checks hold
P-02  ACCEPT   FAIL          R1-baseline: no degenerate baseline reported: cannot rule out a do-nothing policy
P-03  ACCEPT   FAIL          R1-baseline: only the flattering 'no-defence' (always-allow) baseline; no unflattering baseline reported (lopsided reporting)
P-04  ACCEPT   FAIL          R1-baseline: majority-class listed but its score never reported and no post-defence ASR given: comparison is decorative
P-05  ACCEPT   FAIL          R4-metric: scoring rule rewards abstention without charging lost utility: always-abstain scores as well as a perfect defence (degenerate metric)
P-06  ACCEPT   PASS          all checks hold
P-07  ACCEPT   INCONCLUSIVE  R3b-power: n=20: too small to rule out luck (underpowered, not wrong)
P-08  REJECT   INCONCLUSIVE  R3a-counts: rates only, no raw counts: result cannot be recomputed or pooled

Case Study Zero (anonymised teaching illustration):
  reported ranking: policy_E (0.67) > policy_F (0.33)
  rescored ranking: policy_F (0.92) > policy_E (0.75)
  -> the ranking INVERTS once verdicts are scored against sealed labels
```

**Compare with your Step 1 predictions.** Two things to notice:
1. The naive reviewer accepts **7 of 8** — including all four FAILs. Headline numbers are cheap.
2. P-08 is the only paper the naive reviewer rejects (0.06 > 0.05) — yet the auditor calls it INCONCLUSIVE, not failed. A bad threshold can reject the honest-but-thin paper while accepting every broken one.

---

## Step 4 — Generate the Results File

```bash
python3 student/generate_audit_results.py
```

**Expected:** prints the full `audit_results.json` document and writes it to `results/audit_results.json`, ending with `"result": "pass"`. The file records demo name, seed (42), commit, environment, per-paper verdicts with reasons, and the Case Zero rescore.

**Verify:**

```bash
python3 -c "import json; d=json.load(open('results/audit_results.json')); print(d['result'], '| papers:', len([r for r in d['results'] if r['paper_id'].startswith('P-')]), '| inversion:', d['case_study_zero']['ranking_inverts'])"
# Expected: pass | papers: 8 | inversion: True
```

---

## Step 5 — Rescore Case Study Zero by Hand

Run this and check you can reproduce the inversion without the script:

```bash
python3 - <<'EOF'
import json
case = json.load(open('fixtures/case_zero.json'))
labels = case['sealed_labels']
ids = list(labels)
rep = case['reported_verdicts']
for p, v in rep.items():
    buggy = sum(1 for x in v if x == 'malicious')
    true = sum(1 for x, i in zip(v, ids) if x == labels[i])
    print(f"{p}: reported {buggy}/12, rescored {true}/12")
EOF
# Expected:
# policy_E: reported 8/12, rescored 9/12
# policy_F: reported 4/12, rescored 11/12
```

**Why it matters:** the buggy scorer rewarded saying MALICIOUS (8 of E's 12 verdicts). Against sealed labels, E's near-degenerate strategy scores 9/12 while the honest policy F scores 11/12. The published ranking (E > F) was an artefact of the scorer, not a property of the defences.

---

## Step 6 — Exercises

### Exercise 11.1 — Score the degenerate policy (5 min)
Using only `fixtures/case_zero.json`: what does a policy that says MALICIOUS on all 12 items score against the sealed labels? What does it score under the published (buggy) scorer? Write two sentences explaining why the buggy scorer cannot rank defences. (Answer key: `solutions/audit_walkthrough.md`. Covered by `test_exercise_always_allow_on_case_zero`.)

### Exercise 11.2 — Break P-05's metric (3 min)
P-05's scoring rewards abstention without charging lost utility. Describe a policy that achieves a perfect score under that metric while providing zero utility, and state the one-line fix to the metric. (Covered by `test_exercise_always_block_beats_P05_metric`.)

### Exercise 11.3 — Write the review verdict (5 min)
Pick P-03 or P-04. Write a three-sentence peer-review verdict: (1) what the paper claims, (2) which audit rule it violates and why, (3) the single experiment or analysis that would fix it. Compare with `solutions/audit_walkthrough.md`.

---

## Reproducibility Protocol (for study participants)

1. Record your environment: `python3 --version`, OS, and `git rev-parse --short HEAD` (or `local`).
2. Run Steps 2–4 in order; save the full terminal output to a file.
3. The auditor is deterministic — re-running must produce byte-identical output (enforced by `test_results_are_deterministic`).
4. Submit: terminal output + `results/audit_results.json` + your Step 1 prediction table + Exercise 11.3 verdict.
5. Do not edit fixtures to make verdicts change; if you believe a verdict is wrong, file it as a finding with the rule number.
