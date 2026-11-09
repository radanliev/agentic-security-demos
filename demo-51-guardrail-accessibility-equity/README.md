# Demo 51: Guardrail Accessibility Equity

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain how guardrail false positives can fall unevenly on assistive-technology text
- Compute per-variant false-positive and detection rates, smoothed disparity and paired flip rates
- Fit audit-only thresholds under a detection floor and identify conflicts
- Explain why per-variant thresholds are an audit instrument, not a deployable policy
- Distinguish teaching demonstrations from validated research benchmarks

**Status:** design stage, created 6 November 2026. The repository holds offline audit functions,
synthetic placeholder scores and tests. It holds no results; every empirical statement in a future
paper is [RESULT PENDING] until a committed analysis script derives it.

## Research question

Do the input guardrails that screen untrusted text before an agentic AI system acts on it flag
benign text written with, or produced by, assistive technologies more often than equivalent
standard text, and can a screening policy reduce that disparity without lowering the detection of
policy-violating inputs below a stated floor?

## Why it matters

Guardrails are tuned on corpora of standard written English. Text produced through speech-to-text,
augmentative and alternative communication (AAC) devices, or by writers with dyslexia, and text
rewritten into plain language, can differ from that norm in ways a classifier may read as
anomalous. If such text is blocked more often, the learners who most need an accessible service
are refused it, which engages equality and accessibility duties as well as security design
[CITATION NEEDED: independent sources on guardrail and content-classifier bias, and on assistive
technology text characteristics].

## Measures implemented

| Function | Measure |
|---|---|
| `rates` | per-variant false-positive rate on benign text and detection rate on violating text |
| `disparity` | ratio of each variant's smoothed false-positive rate to the standard variant's |
| `paired_flip_rate` | share of counterfactual pairs where the standard text passes and the variant text is flagged |
| `fit_thresholds` | audit-only per-variant thresholds that equalise false-positive rates, kept only when a detection floor holds; otherwise the variant is reported as a conflict |

The per-variant fit is an audit instrument: it shows how much of a disparity a threshold change
could remove. It is not a deployable policy, because a deployed guardrail must not infer
disability or assistive-technology use. Deployable mitigations considered in the study are
variant-agnostic.

## What is here now

| Path | Contents |
|---|---|
| `student/guardrail_equity/` | the audit functions above |
| `fixtures/synthetic_scores.json` | hand-written placeholder scores for five variants; no text, model or person stands behind them |
| `student/run_equity.py` | prints the audit table and writes `results/guardrail_equity.json` |
| `tests/` | unit tests (standard library `unittest`; also collected by pytest) |

```bash
python3 student/run_equity.py
python3 -m pytest tests/ -v
```

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic placeholder scores only.**
- No real text, people, models, or credentials
- No network access (standard library only)
- All scores are hand-written toys
- Results demonstrate a mechanism; they are not evidence about real guardrails or real communities

## Distinctness

- Demo 37 (detector cost) compares prompt-injection detectors on aggregate false-positive cost;
  demo 51 measures disparity between writing variants under a paired counterfactual design and
  tests mitigations against a detection floor.
- Demo 18 (cross-lingual gap) studies language transfer; demo 51 holds the language fixed and
  varies accessibility-related surface style.

## Venue plan

Plan A (proposal): IJCAI 2027 (main track or the AI for Social Good special track, same dates), abstract 4 January 2027 and papers 11 January 2027 AoE, 7 body pages plus 2 reference pages ([CFP](https://2027.ijcai.org/ijcai-2027-call-for-papers-main-track/), checked 9 November 2026). If the manuscript cannot fit 7+2 pages, the next published option is Plan B: USENIX Security 2027 Cycle 2, 13-page body, registration 19 January 2027 and papers 26 January 2027 ([CFP](https://www.usenix.org/conference/usenixsecurity27/call-for-papers), checked 9 November 2026). Plan C: ACM FAccT 2028 — the 2027 full-paper deadline has passed and the 2028 call is unpublished. SOUPS 2027 and ASSETS 2027 calls were not verified as published at the time of checking.

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 51 (fixed; no randomness used unless a test says otherwise) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=51` |

## Reproducibility

```bash
python3 -m pytest tests/ -v      # 7 tests
python3 student/run_equity.py    # writes results/guardrail_equity.json
```

Python 3.11 or newer, standard library only, fully offline and deterministic.

## Licence

MIT (see the repository [LICENSE](../../LICENSE)).
