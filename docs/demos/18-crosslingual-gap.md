# Demo 18: Crosslingual Gap

## Learning Objectives

- Explain the crosslingual injection gap (English-tuned detectors miss non-English payloads)
- Apply one English-centric rule plus a single marker to 10 synthetic payloads
- Show recall EN 4/4 vs non-EN 2/6 (total 6/10)
- Distinguish this teaching toy from the preregistered study it illustrates (no data collected there yet)

## Conceptual Explanation

Many detectors key on English phrasing. Paraphrase or translate the payload and the same intent slips through. One language-agnostic marker catches a fraction of the transfer cases but not all. This toy uses 10 hand-built payloads (EN 4, ES 2, ZH 2, AR 2): English recall is perfect (4/4); non-English recall is 2/6.

Boundary: this demo is language transfer of fixed payloads; it is not detector tuning or cost analysis (Demo 37). Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real payloads, models, or credentials
- No network access (standard library only)
- All payloads, detections and verdicts are hand-built toys

## Run It

```bash
cd demo-18-crosslingual-gap
python3 -m pytest tests/ -v          # 5 tests, <1 min
python3 student/run_lang.py          # writes results/lang_gap.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-18-crosslingual-gap/INSTRUCTIONS.md).
