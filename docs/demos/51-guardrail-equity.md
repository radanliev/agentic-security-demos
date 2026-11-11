# Demo 51: Guardrail Equity

## Learning Objectives

- Explain why one global input-guardrail threshold can be inequitable
- Compute false-positive rate (FPR) disparity ratios across writing variants
- Contrast detection quality (TPR) with collateral burden (FPR)
- Connect the toy to accessibility justice for AAC and dyslexia-pattern writing
- Distinguish teaching demonstrations from validated research benchmarks

## Conceptual Explanation

One guardrail, one threshold (0.5), five synthetic writing variants. Every
variant catches all planted policy violations (TPR 1.0) — but the benign
false-positive burden is wildly uneven.

| Variant | Benign FPs | FPR | Disparity vs standard |
|---------|-----------|-----|----------------------|
| standard | 0/4 | 0.00 | 1× |
| plain_language | 1/4 | 0.25 | 3× |
| speech_to_text | 2/4 | 0.50 | 5× |
| dyslexia_pattern_spelling | 2/4 | 0.50 | 5× |
| aac_telegraphic | 3/4 | 0.75 | 7× |

The security property (catching violations) is identical everywhere; the
accessibility cost is not. Telegraphic AAC writing is punished hardest for
the same protection.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real users, assistive technologies, or providers
- No network access (standard library only)
- All utterances are hand-built toys
- Results demonstrate a mechanism; they are not evidence about real guardrails

## Run It

```bash
cd demo-51-guardrail-accessibility-equity
python3 -m pytest tests/ -v          # 7 tests, <1 min
python3 student/run_equity.py        # writes results/guardrail_equity.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-51-guardrail-accessibility-equity/INSTRUCTIONS.md).

## Relationship to Demo 37

Demo 37 compares detectors on cost and accuracy; this demo holds one detector
fixed and asks who pays for its false positives.
