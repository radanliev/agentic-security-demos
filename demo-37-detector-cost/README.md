# Demo 37: Detector Cost

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain why detector choice is an operating-point decision, not an accuracy contest
- Score a strict substring detector and a lenient exact-phrase detector on the same 10 synthetic prompts
- Price false positives at 10 and false negatives at 25, and show the strict detector wins on cost (20 vs 50)
- Distinguish this teaching toy from the pending Computers & Security practitioner evaluation it illustrates

## Conceptual Explanation

A detector that catches everything also cries wolf. On these 10 hand-built
prompts (4 injected, 6 benign), the strict rule (`ignor*` substring) catches
4/4 injections but false-alarms on 2/6 benign prompts, including two tricky
ones: a request to "ignore the previous email thread" (benign context) and a
mention of "the ignore button". The lenient rule (exact phrase "ignore
previous instructions") misses the 2 paraphrased injections but never
false-alarms.

| Detector | TP | FP | FN | Cost (FP=10, FN=25) |
|----------|----|----|----|----------------------|
| Strict | 4/4 | 2/6 | 0/4 | 2×10 + 0×25 = 20 |
| Lenient | 2/4 | 0/6 | 2/4 | 0×10 + 2×25 = 50 |

Lesson: under asymmetric costs, the noisier detector is the cheaper one.
Tune the threshold with costs, not accuracy.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real prompts, models, detectors, or credentials
- No network access (standard library only)
- All prompts, flags and costs are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real detectors

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 37 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=37` |

## Research Connection

This demo illustrates the design question of a practitioner evaluation of
prompt-injection detectors (targeting Computers & Security). That evaluation
is **pending**; every quantity there is `[RESULT PENDING]`. Nothing here
describes a publication, a venue result, or a measured effect size.

Provenance: distilled from `demo-37-prompt-injection-detectors-evaluation-cose` (private research repo).
It shares no topic with Demo 18 (language transfer): this demo is detector
OPERATION priced with false-positive cost; Demo 18 studies cross-language
transfer. Different questions, data, and claims.

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | Practitioner detector benchmark (pending) | 10 hand-built prompts |
| Method | Multi-detector evaluation with cost modelling | Two substring rules, fixed FP=10/FN=25 |
| Claims | Falsifiable detector-ranking hypotheses | **No claims** — mechanism illustration only |
| Artefact | Evaluation harness over real detectors | Two tiny detector functions |
