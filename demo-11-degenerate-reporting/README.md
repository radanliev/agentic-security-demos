# Demo 11: Degenerate Reporting

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output, plus a reproducibility protocol for study participants.

## Learning Objectives

- Explain why an evaluation without a degenerate (do-nothing) baseline proves nothing about a defence
- Distinguish flattering baselines ("no defence") from unflattering ones (always-block, random, majority-class)
- Show why accuracy-style claims are unknowable without base rates and raw counts
- Detect metrics that reward doing nothing (e.g. abstention without a utility charge)
- Rescore published verdicts against sealed labels and watch a ranking invert

## Conceptual Explanation

**Degenerate reporting** is an evaluation failure mode: a defence paper reports numbers that a trivial, do-nothing policy could also produce — and never runs the trivial policy, so nobody notices.

A **degenerate (do-nothing) baseline** is a policy with no intelligence in it:

| Baseline | What it does | Why it matters |
|---|---|---|
| `always-allow` | Admits everything | Any defence must beat "do nothing" |
| `always-block` | Denies everything | Any defence must beat "refuse everything" |
| `random` | Decides by coin flip | Any defence must beat chance |
| `majority-class` | Always predicts the common class | Any defence must beat the base rate |

If a paper reports none of these *with scores*, its headline number floats free: a 0.03 attack-success rate means nothing if always-allowing everything also scores 0.03 on the same (easy) trials.

### Three classic failure shapes

1. **No baseline at all (P-02).** The paper reports a post-defence number with nothing to compare it to. A do-nothing policy is never ruled out.
2. **Lopsided reporting (P-03).** The paper reports only the *flattering* baseline — "no defence", which is always-allow under a kind name and looks bad, so the defence looks good. It never reports an *unflattering* baseline (always-block, random) that a policy of "deny more" could also beat.
3. **Decorative comparison (P-04).** The baseline is *named* (majority-class) but its score is never reported — the comparison is decoration, and without a base rate the headline accuracy is unknowable anyway.

### Two subtler failure shapes

4. **Degenerate metric (P-05).** The scoring rule itself rewards doing nothing: abstention is rewarded without charging lost utility, so an always-abstain policy scores as well as a perfect defence. No baseline can save a metric that cannot see degeneracy.
5. **Thin evidence (P-07, P-08).** The right baselines are reported, but `n=20` cannot rule out luck (underpowered — inconclusive, not wrong), or only rates are published with no raw counts (not recomputable, not poolable).

### Case Study Zero (anonymised teaching illustration)

A defence paper's scorer equated "verdict correct" with "said MALICIOUS". Under that scorer, policy E (8/12) beat policy F (4/12). Rescored against the sealed labels, E scores 9/12 and F scores 11/12 — **the ranking inverts**. Policy E was rewarded for saying MALICIOUS almost everywhere, a near-degenerate strategy the scorer could not see. All numbers here are a synthetic illustration, not measurements from any real system.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- All eight "papers" are invented; titles, numbers and verdicts describe no real publication
- Case Study Zero is anonymised and fully synthetic — it names no system, author, or venue
- No network access, no credentials, no real paper titles
- Results are demonstrations, not validated research claims

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 42 (fixed; the auditor is deterministic — no randomness anywhere) |
| Commit | Git SHA or `local` |
| Python | 3.11+ |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=11` |

## Conference Paper Alignment (Paper 11: RAID)

This demo is the educational companion to **Conference Paper 11** (`demo-11-degenerate-reporting-raid`):
> **Indistinguishable from Doing Nothing: Degenerate Reporting in Indirect Prompt-Injection Defence Evaluation** (RAID)

### Concept Mapping

| Demo Element | Research Paper Element |
|---|---|
| 8-paper fixture audit (P-01–P-08) | Literature coding study: how rarely published defences report trivial baselines |
| PASS / FAIL / INCONCLUSIVE verdicts | Strict vs. lopsided-reporting readings of the field |
| Case Study Zero rescore | Anonymised instance of a scoring bug inverting a ranking |
| Metric-sanity check (R4) | Degenerate-metric analysis (abstention-style remedies) |
| Thin-evidence verdicts (P-07, P-08) | Reproducibility census: cells that cannot be recomputed |

### Why the Naive Reviewer Accepts 7/8 and the Auditor Passes 2/8

- **Naive Reviewer (headline reader)**: Accepts any paper whose reported post-defence attack rate is at most 5%. It accepts **7 of 8** — every FAIL in the fixture. That is the point: headline numbers are cheap.
- **Rigorous Auditor (checklist)**: Passes only papers clearing all four rules. It passes **2 of 8** (P-01, P-06). Notably it *rejects* P-08 (6% — above the naive threshold anyway) as INCONCLUSIVE rather than failed: thin evidence is inconclusive, not wrong.

## Difference from Private Research Benchmark

| Aspect | Research Benchmark (Paper 11) | This Teaching Demo (Demo 11) |
|--------|-------------------------------|------------------------------|
| Data | ~970-candidate systematic search, 129 full-text reads | 8 invented papers + 1 synthetic case study |
| Scale | Multi-agent literature coding with PRISMA counts | Deterministic 4-rule checklist, runs in <1s |
| Claims | Field-wide reporting rates with confidence intervals | Illustrative verdicts; no empirical claims |
| Status | Research paper not yet submission-ready | Teaching demo, complete and self-contained |

> **Honesty note:** the research paper behind this demo is explicitly *not* submission-ready (see its STATUS.md). This teaching demo does not reproduce its measurements and makes no claims about the field — it teaches the *audit method* on synthetic data, so students learn to spot degenerate reporting before they ever review a real paper.
