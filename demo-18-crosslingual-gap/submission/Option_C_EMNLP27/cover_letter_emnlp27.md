# Author Cover Letter — EMNLP 2027

**To**: Program Committee Co-Chairs and Track Chairs  
**Conference**: Conference on Empirical Methods in Natural Language Processing (EMNLP 2027)  
**Track**: Empirical Methods / Security, Privacy, and Robustness in NLP  
**Submission Portal**: Softconf / OpenReview (as specified by EMNLP 2027 CFP)

---

## Submission Details

- **Title**: Empirical Evaluation of Cross-Lingual Prompt Injection: Calibration Disparity and Tokenisation Drift
- **Track**: Empirical Methods in NLP / Security, Privacy, and Robustness
- **Keywords**: prompt injection, empirical NLP, multilingual calibration, tokenisation fertility, safety evaluation
- **Submission Type**: Full Research Paper (EMNLP two-column format)

---

## Abstract

Empirical evaluation of prompt injection defences often assumes that detector calibrations transfer across languages. This paper provides a rigorous empirical analysis of cross-lingual injection detection across 57,912 scored inferences spanning English, Chinese, Arabic, and Spanish. We show that multilingual safety classifiers do not suffer from cross-lingual recall collapse under English-calibrated thresholds. Rather, multilingual encoders exhibit pronounced calibration drift, assigning higher anomaly scores to non-English inputs regardless of intent. Under standard English operating points, benign false-positive rates escalate to 67.7% for Chinese and 15.7% for Arabic. Conversely, conditioning detection thresholds on language restores benign specificity but precipitates severe evasion collapse, reducing Arabic recall from 54.0% to 7.0%. Furthermore, agent execution evaluations over 1,160 episodes demonstrate an empirical floor effect where attack success remains near zero across languages, preventing valid claims of cross-lingual divergence in task execution. Finally, subword tokenisation fertility reaches 4.33x in non-Latin scripts, correlating with score inflation. We formalise these empirical trade-offs and provide methodological recommendations for evaluating multilingual security boundaries.

---

## Author & Anonymous Statement

This paper is submitted in full compliance with the EMNLP double-blind review regulations:
1. No author names, affiliations, or institutional details are revealed in the document or metadata.
2. Code repositories and artifact releases have been completely anonymised.
3. Explicit Limitations and Ethics sections are incorporated in accordance with ACL/EMNLP author guidelines.

---

## Submission Intent & Sequential Fallback Policy (Plan C)

The authors confirm their intention to submit this manuscript via the official EMNLP submission system.

**Sequential Fallback Policy**: This submission serves as tertiary fallback (Plan C). In accordance with dual submission policies across all participating venues, this package will only be activated if the paper has been rejected sequentially by:
1. The Web Conference 2027 (Plan A, decision expected January 2027), and
2. ACL 2027 via ARR (Plan B, decision expected April 2027).

At no stage will this work be submitted concurrently with an ongoing review process at another venue.
