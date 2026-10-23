# Demo 40: Corpus Union

## Learning Objectives

- Explain what a corpus union is (merge sources, dedupe, licence-gate)
- Normalise 12 synthetic records (lowercase + strip) and dedupe by SHA-256 to 9 unique texts
- Apply a licence gate (permissive + by-sa only) releasing 7/9 records
- Distinguish corpus INFRASTRUCTURE (this toy) from any measurement claim

## Conceptual Explanation

Sharing a security corpus means answering two questions: what is duplicated, and what may be released? On 12 hand-built records from sources A/B/C:

| Stage | Count |
|-------|-------|
| Ingested records | 12 |
| Unique after SHA-256 dedupe | 9 (3 cross-source duplicates removed) |
| Releasable (permissive + by-sa) | 7/9 |
| Blocked | r07 (noncommercial), r08 (unlicensed) |

The lesson: dedupe decides what the corpus *is*; the licence gate decides what it may *become*. Neither step says anything about the world outside the fixture.

Boundary: this demo is corpus infrastructure with no measurement claim; it is not detector evaluation (Demo 37). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real datasets, licences, or credentials
- No network access (standard library only)
- All records, texts and verdicts are hand-built toys

## Run It

```bash
cd demo-40-corpus-union
python3 -m pytest tests/ -v          # 6 tests, <1 min
python3 student/run_corpus.py        # writes results/corpus.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-40-corpus-union/INSTRUCTIONS.md).
