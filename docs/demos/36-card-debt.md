# Demo 36: Model Card Debt

## Learning Objectives

- Explain documentation debt (model cards missing safety, provenance, or license sections)
- Count 7/12 synthetic cards missing a safety section
- Show the popularity gap: top-4 miss 1/4 while bottom-8 miss 6/8
- Distinguish card disclosure from lineage risk (Demo 19)

## Conceptual Explanation

Model cards should disclose safety-relevant facts, but the long tail often skips them. This toy audits twelve hand-built cards ranked by downloads: 7/12 missing a safety section; top-4 by downloads miss 1/4 while bottom-8 miss 6/8. Popular cards disclose more often; the tail carries the debt.

Boundary: this demo covers card disclosure only, not lineage risk (Demo 19).

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real cards, registries, models, or credentials
- No network access (standard library only)
- All cards and verdicts are hand-built toys

## Run It

```bash
cd demo-36-card-debt
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_cards.py         # writes results/cards.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-36-card-debt/INSTRUCTIONS.md).
