# Module 11: Degenerate Reporting (Extension)

**Duration**: 1 hour | **Format**: Demo (15 min) + Exercises (30 min) + Review-writing (15 min)
**Prerequisites**: Modules 3 (Evaluation Invariants), 7 (TriageTrap)
**Demo directory**: `demo-11-degenerate-reporting/`

> Extension module: take it after Module 10, before the Final Assessment. It teaches you to audit *any* evaluation — including your own portfolio work — before you submit it.

---

## 🎯 Learning Goals

By the end of this module you can:
1. Name the four degenerate baselines and say what each rules out
2. Spot lopsided reporting (flattering baseline only) and decorative comparisons
3. Explain why accuracy without a base rate is unknowable
4. Detect a metric that rewards doing nothing
5. Write a three-sentence review verdict that names the violated rule and the fix

## 🧪 Demo Script (15 min, facilitator runs)

Follow [`demo-11-degenerate-reporting/INSTRUCTIONS.md`](../../demo-11-degenerate-reporting/INSTRUCTIONS.md) Steps 0–5 live. Pause at two moments:

1. **After Step 1 (predictions):** poll the room — how many papers will the auditor pass? Most cohorts guess 5–7. The answer (2) lands harder for having predicted first.
2. **After Step 3 output:** ask *why the naive reviewer rejects P-08 but accepts P-02.* (Answer: the 5% threshold punishes the honest-but-thin paper and rewards every broken one. Thresholds are not audits.)

## 📝 Exercises (30 min, students work in pairs)

- **Exercise 11.1** — Score the degenerate policy against sealed labels (INSTRUCTIONS Step 6).
- **Exercise 11.2** — Break P-05's metric: describe the perfect-scoring do-nothing policy and the one-line fix.
- **Exercise 11.3** — Write a three-sentence review verdict for P-03 or P-04.

Walkthrough with worked answers: [`demo-11-degenerate-reporting/solutions/audit_walkthrough.md`](../../demo-11-degenerate-reporting/solutions/audit_walkthrough.md) (release *after* the session).

## 🔗 Links to Earlier Modules

| This module revisits | Connection |
|---|---|
| Module 1 (Blind Verification) | A scorer that cannot see degeneracy is an oracle that leaks: same failure shape as post-hoc commitments |
| Module 3 (Eval Invariants) | R1–R4 are executable invariants for *reporting*, complementing Module 3's invariants for *measurement* |
| Module 7 (TriageTrap) | Base rates (R2) and the "metadata ≠ evidence" discipline, applied to papers instead of artifacts |
| Final Assessment | Use the four-rule checklist on your own portfolio results before submitting them |

## ✅ Completion Criteria

- `results/audit_results.json` shows `"result": "pass"` with 8 papers audited and `ranking_inverts: true`
- Step 1 prediction table filled *before* running (not after)
- Exercise 11.3 verdict submitted (three sentences, names the rule and the fix)
