# Demo 57: Governance Corpus

## Learning Objectives

- Build a small corpus of synthetic higher-education AI-policy excerpts
- Apply a fixed codebook with two independent synthetic raters
- Compute percent agreement and Cohen's κ
- Explain why κ < percent agreement (chance agreement is not agreement)
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Six synthetic policy excerpts, one codebook, two raters.

| Quantity | Value |
|----------|-------|
| Excerpts | 6 |
| Invalid codes | 0 |
| Percent agreement | 0.667 |
| Cohen's κ | 0.571 |

Percent agreement counts every match, including matches the codebook's base
rates would produce by chance; κ discounts those. A κ near 0.57 with 67% raw
agreement is a moderate, honest codebook for a toy — and the gap between the
two numbers is the lesson.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real institutions, policies, or raters
- No network access (standard library only)
- All excerpts and ratings are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real governance

## Run It

```bash
cd demo-57-he-governance-corpus
python3 -m pytest tests/ -v          # 3 tests, <1 min
python3 student/run_coding.py        # writes results/coding.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-57-he-governance-corpus/INSTRUCTIONS.md).

## Relationship to Demos 43 and 58

Demo 43 codes platform terms for accountability; demo 58 measures task-level
work exposure. This demo is the measurement layer underneath both: how
codes and agreement are validated before any claim is made.
