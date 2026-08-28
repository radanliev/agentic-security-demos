# Final Assessment

**Duration**: 2 hours | **Format**: Quiz (45 min) + Practical (45 min) + Reflection (30 min)
**Prerequisites**: Modules 0–10

---

## 📋 Assessment Structure

| Component | Time | Weight | Submitted |
|-----------|------|--------|-----------|
| **Part A: Written Quiz** | 45 min | 15% of course grade | `FINAL_QUIZ_ANSWERS.md` |
| **Part B: Integration Practical** | 45 min | Graded pass/redo | New code + test + results JSON |
| **Part C: Reflection Report** | 30 min | 10% of course grade | 2-page `REFLECTION.md` |

---

## 📝 Part A: Written Quiz (25 questions)

Answer in `FINAL_QUIZ_ANSWERS.md`. Closed-book except: you may consult *your own* `LAB_NOTES.md`.

### Section 1 — Blind Verification (Modules 1, 3)

**Q1.** In one sentence: why does a 4/4 score from an agent that read the oracle measure nothing about capability?

**Q2.** Demo 01's oracle for `authz-001` checks that the commitment *contains* the string `AuthorizationError`. Describe a commitment that passes this oracle but does not fix the vulnerability.

**Q3.** Module 3's four-arm table shows the baseline agent at 0.88 and the verified agent at 0.81 with invariants ignored; with invariants run, both get the same 3/5 verdict on this evaluation (the leaked item is `task-003`), and the clean-item means are 0.85 and 0.84. Which result would you ship to a customer, and why in two sentences?

**Q4.** Name the five evaluation invariants and the single failure mode each is designed to catch.

### Section 2 — Governance & Policy (Module 2)

**Q5.** State the four-rung decision order of the AIBOM policy gate and give one attack stopped at each rung.

**Q6.** Why does `waiver_rules.allowed_scopes` exist? What specifically breaks if any scope can be waived?

**Q7.** A waiver is approved, scoped to `exec:tools:scanner`, and expires in 10 minutes. Give one operational risk this creates and one control that mitigates it.

### Section 3 — Authority & Provenance (Modules 4, 6, 7, 8)

**Q8.** Define the confused-deputy problem in one sentence, then map each element (deputy, authority, attacker) onto Demo 04's tool loop.

**Q9.** Demo 04's scope tokens use prefix matching. You showed `/workspace/../etc/passwd` passes. Explain *why* prefix matching fails here and name the general fix.

**Q10.** In Module 6, the defended agent *logs* injections from HTTP headers rather than executing them. State the provenance rule that produces this behavior, exactly as the code enforces it.

**Q11.** Module 7: art-004 contains zero malware but the baseline quarantines it. Trace the four-step code path (detector → ? → ? → threshold) that turns a string into a fleet-wide action.

**Q12.** State the Module 8 thesis. Then give the attack that scope alone misses — i.e., malicious content that lives *inside* an allowed path glob.

**Q13.** Both Modules 6 and 8 screen content for injection. Give one reason the *same* regex detector is acceptable in Demo 7's architecture but dangerous if it were the *sole* defense in Demo 8's.

### Section 4 — Cryptographic Evidence (Module 5)

**Q14.** Demo 05's `verify_trace` accepted a tampered trace. Explain precisely what a hash chain does and does not prove, and name the mechanism from the module that closes the gap.

**Q15.** A forger deletes step 4 *and* updates closing counts to 5. Which verifier expectation still catches this, and where must that expectation live to be trustworthy?

**Q16.** A Merkle proof for a 6-leaf tree has how many sibling nodes? For one million leaves, approximately how many? Why does this matter for transparency-log design?

**Q17.** `DemoKeyManager.generate_key` refuses ids without the `DEMO_KEY_` prefix. What production discipline does this encode, and what goes wrong in real systems without it?

### Section 5 — Taint & Scanning (Modules 9, 10)

**Q18.** Demo 09's guard has two rules: a per-action taint ceiling, and "a privileged action (ceiling LOW) never accepts `intercepted_network` provenance, whatever the taint label says." Construct an input blocked by rule 2 but allowed by rule 1 alone (the run's `frame_001_relabelled_low` is one), and state the attack rule 2 exists for.

**Q19.** In Demo 10, check_003 is rejected by the validator and never executed, so there is nothing of it to taint-track, whereas check_001 is executed, its finding is tainted HIGH from its own text, and the action policy then holds the report. Explain the observation-vs-action distinction the pipeline encodes, and why a rejected check has nothing to observe.

**Q20.** Give one payload that Demo 10's keyword screen cannot catch but its AST screen does, and explain why no keyword list can ever be sufficient.

### Section 6 — Synthesis

**Q21.** Five modules used the pattern "default deny, escalate with justification" (policy gate, mediator, inclusion guard, action guard, release gate). State the pattern once, generically, and name the *one* component every implementation shared.

**Q22.** Three modules discovered a gap in their own defense during the lab (prefix-scope traversal, string oracle false positives, self-consistent chain forgery). For each: the gap, and the fix's *general principle*.

**Q23.** A teammate proposes adding live network scanning to Demo 06 "to make it realistic." Write a 3-sentence refusal grounded in (a) the repository's safety guarantees, (b) legal exposure, and (c) what the offline version already teaches.

**Q24.** Which single module changed your mental model of agentic AI security the most? What was the before/after?

**Q25.** The course's demos share a result schema (demo, experiment, seed, commit, environment, command, result, notes). Give one concrete incident where omitting `commit` or `environment` would make a result unreproducible or misleading.

---

## 🛠️ Part B: Integration Practical

**Task**: Build **`demo-11-memorybound/`** — a minimal module defending agent *memory* against poisoning, reusing at least three patterns from the course.

### Requirements

Your module must include:

1. **`fixtures/memory.json`** — synthetic memory entries:
   - ≥3 benign entries (`user_data` provenance)
   - ≥2 poisoned entries containing instruction-shaped canaries (`untrusted_retrieval` provenance)
   - 1 entry with a *stale* timestamp (older than a configurable freshness window)

2. **`student/memorybound.py`** implementing:
   - A `MemoryStore` that stores `(content, provenance, timestamp)` and **fails closed** on retrieval of entries missing any field
   - A `PoisonDetector` (reuse your Module 7/8 pattern-matching approach)
   - A `RecallAgent` with a **retrieval policy**: poisoned entries may be *retrieved as evidence* but flagged; instruction-shaped content may never be *promoted to instructions*; stale entries require explicit `allow_stale=True`

3. **`tests/test_memorybound.py`** with ≥6 tests, including:
   - Poisoned entry retrieved-but-flagged (not executed)
   - Stale entry blocked without override
   - Missing-provenance entry rejected (fail-closed)
   - A pinned *vulnerable* baseline that promotes poisoned content (Module 4/7 style specimen)
   - A no-network-imports safety test (grep the source, Module 0 style)

4. **`student/generate_results.py`** emitting the standard result schema

5. **`Makefile`** with `setup` / `test` / `demo` / `clean`

6. **`README.md`** with objectives, safety notice, and the standard reproducibility block

### Grading the practical

| Criterion | Pass | Excellent |
|-----------|------|-----------|
| Runs | `make test` passes; `make demo` produces results JSON | + `make verify-safety` passes with the new module registered |
| Defense correctness | All four behavior requirements demonstrated | Each has a *pinned* test with a distinct reason string |
| Course patterns | ≥3 patterns reused with attribution in comments (e.g., "fail-closed per Module 4 Ex 4.5") | + one pattern *extended* beyond its source module |
| Safety | No network imports; no exec/eval; synthetic only | + safety test greps its own source (self-verifying) |
| Schema | Standard JSON emitted | + provenance chain included per decision (Module 7 style) |

**Time guidance**: skeleton (10 min) → store+detector (15 min) → agent policy (10 min) → tests (10 min). If you finish early, add the stale-override *audit log* (who allowed stale, when — Module 10 Exercise 10.2 pattern).

---

## ✍️ Part C: Reflection Report

Write 2 pages (`REFLECTION.md`) addressing:

1. **The defense that was hardest to get right.** Pick one mechanism from the course (e.g., fail-closed on missing provenance, taint ceilings, waiver scoping). Explain *why* it was conceptually hard — what makes the insecure version attractive?

2. **Where the course's defenses would break first in production.** Choose one demo and describe the most realistic gap between its model and a deployed system (e.g., provenance labels lost in a summarizer; taint refinement rules drifting; allowlists rotting). What operational control would you add first?

3. **What "safe evaluation" now means to you.** Before this course vs after: complete the sentence "A benchmark score is trustworthy only when…" in ≤2 sentences, then justify using one concrete number or test from your lab notes.

**Grading**: depth of reasoning over length. Specific references to your own lab outputs (file names, scores, reason strings) are strongly rewarded.

---

## 📦 Submission Checklist

- [ ] `FINAL_QUIZ_ANSWERS.md` — 25 answers
- [ ] `demo-11-memorybound/` — complete module per spec
- [ ] `REFLECTION.md` — 2 pages
- [ ] `LAB_NOTES.md` — all 11 module blocks complete with reproducibility fields
- [ ] All demo `results/` directories populated (Modules 1–10)
- [ ] Repository state: `make test` green (all existing suites + your new tests), `make verify-safety` green
- [ ] Git log shows incremental commits (not one final dump)

---

## 🎓 Certification of Completion

Students completing all components meet the course learning outcomes stated in [COURSE_GUIDE.md](COURSE_GUIDE.md). Instructors: record final grades against the rubric in the course guide (Lab Completion 40% / Portfolio 35% / Quiz 15% / Reflection 10%).

---

**⬅️ Prev: [Module 10](lab-10-scanbound.md) | ↩️ Back to: [Course Guide](COURSE_GUIDE.md)**
