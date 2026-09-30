# Demo 14: Conformal Action Gating

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

<p align="center">
  <img src="https://img.shields.io/badge/Teaching%20demo-Synthetic%20only-blue?style=flat-square" alt="Teaching demo">
  <img src="https://img.shields.io/badge/Python-Stdlib%20only-blue?style=flat-square" alt="Standard library only">
  <img src="https://img.shields.io/badge/Network-Offline%20only-success?style=flat-square" alt="Offline only">
</p>

## Learning Objectives

- Explain what a conformal risk gate is (execute an action only when its risk score is below a calibrated threshold)
- Calibrate a threshold on one episode set to meet a nominal risk budget (alpha 0.30)
- Show the guarantee holds on same-distribution episodes but breaks under benchmark shift
- Distinguish this teaching toy from the preregistered ICML study it illustrates (no data collected there yet)

## Conceptual Explanation

Deployed agents gate every tool call: execute or block. Heuristic thresholds carry no promise.
Conformal risk control picks the threshold from calibration data with a stated budget —
here, at most 30% of executed actions may be injected.

This toy uses 14 hand-built episodes (6 calibration, 4 same-corpus test, 4 shifted test):

| Set | Executed (<=0.20) | Realised risk | Verdict |
|-----|-------------------|---------------|---------|
| Calibration (6) | 2/6 | 0/2 = 0.00 | threshold 0.20 chosen |
| Same-corpus (4) | 1/4 | 0/1 = 0.00 | holds (<= 0.30) |
| Shifted (4) | 2/4 | 2/2 = 1.00 | **fails** — scores mislead under shift |

Episodes `h1`/`h2` are the lesson: injected actions with low scores slip through the
same gate that was safe on the calibration distribution. Coverage measures the
calibration distribution more than deployment safety.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real trajectories, benchmarks, models, or credentials
- No network access (standard library only)
- All episodes, scores and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real gates

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 14 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=14` |

## Research Connection

This demo illustrates the design question of a preregistered study on conformal action
gating for tool-using agents (targeting ICML 2027). That study has **collected no
confirmatory data**; every quantity there is `[RESULT PENDING]`. Nothing here describes
a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-14-conformal-action-gating-icml` (private research repo).
It shares no topic with Demo 15 (MCP ecosystem census): this demo is black-box
statistical gating over action scores; Demo 21 is a measurement census over registry
manifests. Different venues (ICML vs EuroS&P), data, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | AgentDojo, LLMail-Inject, InjecAgent, Agent Security Bench (pending) | 14 hand-built episodes |
| Method | Conformal + weighted correction for covariate shift | Single fixed threshold from 6 calib episodes |
| Claims | Falsifiable coverage hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Calibration kit wrapping any scalar score | Two tiny gate classes |
