# Author Cover Letter — The Web Conference 2027 (WWW'27)

**To**: Program Committee Co-Chairs and Track Chairs  
**Conference**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)  
**Track**: Research Track — Security and Privacy  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)

---

## Submission Details

- **Title**: Prompt Injection Through Web Content: The Span-Only Language Contrast Is Not Scored
- **Track**: Research Track — Security and Privacy
- **Keywords**: prompt injection, Web agents, security and privacy, retrieved content
- **Submission Type**: Full Research Paper (ACM SIGCONF format, 8 pages main text, up to 12 pages total)

---

## Abstract

The security question for autonomous Web agents is whether an untrusted instruction injected into retrieved third-party Web content causes an agent to issue unrequested tool calls, and evades detection when the user prompt remains in English but the retrieved language changes. A bounded evaluation across 1,160 InjecAgent episodes with locally served open-weight models shows attack success is near zero across languages (English 1.7% and 0.0%), falsifying pre-registered hypothesis H1 under a floor effect. No cross-lingual execution gap is claimed. Across 57,912 scored inferences, pre-registered hypothesis H2 is also falsified: open prompt injection detectors do not exhibit cross-lingual recall collapse at English-calibrated thresholds. Instead, multilingual encoders exhibit severe calibration asymmetry that elevates raw injection scores for non-English inputs, inflating false positives on benign text (up to 67.7% false alarms in Chinese and 15.7% in Arabic). Language-conditioned thresholds unmask evasion collapse, dropping Arabic recall from 54.0% to 7.0%. Subword tokenisation fertility reaches 4.33x in non-Latin scripts, identifying an architectural correlate for calibration drift. Defence-in-depth principles for secure Web agent architectures follow directly from these empirical findings.

---

## Author & Anonymous Statement

This manuscript is submitted under the mandatory double-blind review policy of The Web Conference 2027. In compliance with the conference guidelines:
1. All author names, institutional affiliations, and direct identifiers have been omitted from the manuscript and supplementary materials.
2. Any referenced codebase and experimental logs are provided via anonymised repositories without identifying git commit author metadata.
3. The research questions explicitly investigate a core Web problem: indirect prompt injection through retrieved third-party Web content into autonomous Web agents.

---

## OpenReview Intent & Author Cap Compliance

The authors formally declare the intent to register this submission on the official OpenReview portal by the abstract registration deadline of **18 October 2026 23:59 AoE**, followed by final PDF upload before **25 October 2026 23:59 AoE**. 

Furthermore, all listed authors comply with the WWW'27 author cap policy (no author exceeds the maximum limit of seven research-track submissions across the conference).

---

## Dual Submission Declaration

This manuscript presents original, unpublished work. It has not been published elsewhere, nor is it concurrently submitted or under active consideration at any other conference, journal, or workshop. Post-rejection sequential fallbacks (e.g. Plan B via ACL ARR) will only be activated in the event of an explicit rejection decision from WWW'27.
