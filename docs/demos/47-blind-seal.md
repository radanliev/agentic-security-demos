# Demo 47: Pre-Reveal Seal

## Learning Objectives

- Hash a localisation commitment before any ground truth is read
- Chain each seal to the previous seal
- Refuse a commitment whose bytes no longer match the seal (`edited` → commitment_hash_mismatch)

## Conceptual Explanation

A blind evaluation writes the guessed defect id first, seals those bytes, and only then opens the answer key. On three hand-built cases:

| Case | What happens | Verdict |
|------|----------------|---------|
| hit | sealed guess matches the key | hit |
| miss | sealed guess names a different component | miss |
| edited | bytes change after the seal, even if the new text would match the key | commitment_hash_mismatch |

The lesson: a later edit is not a new answer. Scoring never consults the key until the sealed digest still matches.

Boundary: this demo is the seal-before-reveal mechanism on three cases; it is not significance testing of localisation counts (Demo 45). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real vulnerabilities, systems, or credentials
- No network access (standard library only)
- All cases and verdicts are hand-built toys

## Run It

```bash
cd demo-47-blind-seal
python3 -m pytest tests/ -v          # 4 tests, <1 min
python3 student/run_seal.py          # writes results/seals.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-47-blind-seal/INSTRUCTIONS.md).
