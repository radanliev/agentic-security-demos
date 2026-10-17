# Author Cover Letter — ACL 2027 (via ACL Rolling Review - ARR Jan 2027)

**To**: ACL Rolling Review Editors and Action Editors  
**Venue**: 65th Annual Meeting of the Association for Computational Linguistics (ACL 2027)  
**Track / Theme**: ACL Rolling Review — January 2027 Cycle (Theme / Multilingual / Security)  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=aclweb.org/ACL/ARR/2027/January`)

---

## Submission Details

- **Title**: Prompt Injection and Multilingual Representation Disparity: Calibration Asymmetry in Cross-Lingual Safety Evaluation
- **Submission Track**: ACL Rolling Review — January 2027 Cycle
- **Keywords**: prompt injection, multilingual robustness, tokenisation fertility, calibration asymmetry, AI safety
- **Submission Type**: Long Research Paper (ACL two-column format)

---

## Abstract

This study investigates cross-lingual vulnerability and detection dynamics for prompt injection in language models and autonomous agents when input contexts span typologically diverse languages. Evaluating 1,160 InjecAgent episodes under locally served open-weight models reveals near-zero attack success rates across all languages, demonstrating an experimental floor effect rather than genuine cross-lingual robustness. Across 57,912 scored inferences evaluating open injection detectors, cross-lingual recall collapse does not occur at English-calibrated decision thresholds. Instead, multilingual encoders display severe calibration asymmetry: raw injection scores are systematically elevated on non-English text, yielding benign false-alarm rates up to 67.7% in Chinese and 15.7% in Arabic. Applying language-conditioned thresholds causes Arabic detection recall to plunge from 54.0% to 7.0%, revealing an acute trade-off between false-alarm suppression and evasion resistance. Tokenisation fertility analysis indicates up to 4.33x token expansion in non-Latin scripts, highlighting subword fragmentation as a primary correlate of representation drift. These empirical findings indicate that multilingual safety evaluation requires language-specific calibration and script-aware representation auditing.

---

## Author & Anonymous Statement

This manuscript is submitted under the double-blind review policy of the ACL Rolling Review. In strict compliance with ARR guidelines:
1. All author identities, affiliations, and acknowledgments are omitted.
2. The submission conforms to all ARR anonymity requirements, including the anonymisation of supplementary code repositories.
3. Dedicated Limitations and Ethics statements are included in the manuscript following the main body.

---

## OpenReview Intent & Sequential Submission Declaration

The authors declare their intention to submit this manuscript to the ARR January 2027 cycle upon activation.

**Sequential Fallback Policy (Plan B)**: This submission is designated strictly as Plan B. It remains dormant and will only be activated if the primary Plan A submission to The Web Conference 2027 (WWW'27) receives a rejection decision (expected 04 January 2027). Under no circumstances will this manuscript be submitted concurrently while under review at WWW'27.
