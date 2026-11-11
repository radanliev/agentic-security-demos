# Demo 56: Learning Meta-analysis

## Learning Objectives

- Pool k=4 synthetic effect sizes with inverse-variance weighting
- Compute the fixed-effect summary mean and its standard error
- Read a homogeneity statistic (Q on df=3)
- Explain why pooling cannot rescue biased primary studies
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

Four synthetic study rows enter a fixed-effect meta-analysis.

| Quantity | Value |
|----------|-------|
| Studies (k) | 4 |
| Summary mean | 0.345 |
| Summary SE | 0.079 |
| Q (df=3) | 2.12 |

Q below its degrees of freedom signals no detectable heterogeneity, so the
fixed-effect summary is arithmetically fine — and entirely a toy. The effect
sizes are synthetic by construction; the lesson is the machinery, not the
number.

## Safety Notice

⚠️ **Teaching demonstration only.**
- Effect sizes are synthetic; no published study is summarised
- No network access (standard library only)
- Results demonstrate a mechanism; they are not evidence about any literature

## Run It

```bash
cd demo-56-learning-metaanalysis
python3 -m pytest tests/ -v          # 3 tests, <1 min
python3 student/run_meta.py          # writes results/meta.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-56-learning-metaanalysis/INSTRUCTIONS.md).

## Relationship to Demo 35

Demo 35 regresses across benchmarks; this demo pools across studies — two ways
evidence aggregates, both feeding the same lesson about what aggregates can
and cannot say.
