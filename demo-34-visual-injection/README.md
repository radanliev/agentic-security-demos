# Demo 34: Visual Prompt Injection

> **▶️ New here? Follow the step-by-step [Execution Instructions](INSTRUCTIONS.md)** — every command with expected output.

## Learning Objectives

- Explain typographic visual injection (rendered text in an image the agent acts on)
- Show the baseline acts on all 3/3 injections in the untrusted region
- Show a region defense (ignore untrusted) blocks 3/3 injections at a cost of 1 benign
- Distinguish the visual channel from text detectors (Demo 37)

## Conceptual Explanation

Vision-language agents read text rendered inside images. This toy uses eight
hand-built images: three injections (typographic, untrusted, acted) and five
benign, of which one benign in the untrusted region is also acted upon.

| Policy | Injections blocked | Benign cost |
|--------|--------------------|-------------|
| Baseline (act on all typographic) | 0/3 (3/3 succeed) | 0 |
| Region defense (ignore untrusted) | 3/3 | 1 (v07) |

The defense is perfect on injections but not free: it also drops one benign
image the baseline handled.

## Safety Notice

⚠️ **This is a teaching demonstration using synthetic fixtures only.**
- No real images, models, screenshots, or credentials
- No network access (standard library only)
- All images and verdicts are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real agents

## Reproducibility Metadata

| Field | Value |
|-------|-------|
| Seed | 34 (fixed; no randomness used) |
| Python | 3.11+ (stdlib only) |
| OS | Linux/macOS/Windows |
| Command | `make demo DEMO=34` |

## Research Connection

This demo illustrates the benchmark question of a pending study unifying
visual prompt-injection tests targeting IEEE TPAMI. That study has
**collected no confirmatory data**; every quantity there is `[RESULT
PENDING]`. Nothing here describes a publication, a venue result, or a
measured effect size. Boundary: this demo covers the visual channel only, not
text detectors (Demo 37).

Provenance: distilled from `demo-34-visual-prompt-injection-vlm-agents-tpami` (private research repo).

### Difference from the Research Study

| Aspect | Research study | This demo |
|--------|----------------|-----------|
| Data | VLM benchmark suite (pending) | 8 hand-built images |
| Method | Benchmark unification across renderers | Baseline-vs-region-defense count |
| Claims | Falsifiable robustness hypotheses with registered margins | **No claims** — mechanism illustration only |
| Artefact | Unified harness | Two tiny visual helpers |
