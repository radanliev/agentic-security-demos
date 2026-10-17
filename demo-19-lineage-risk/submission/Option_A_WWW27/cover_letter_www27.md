# Author Cover Letter — The Web Conference 2027 (WWW'27)

**To**: Program Committee Co-Chairs and Track Chairs  
**Conference**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)  
**Track**: Research Track — Security and Privacy  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)  
**Date**: 17 October 2026  

---

## Submission Details

- **Title**: What a Client Fetches: Default-Path Exposure of Models Published on the Web
- **Track**: Research Track — Security and Privacy
- **Keywords**: Web security, provenance, model hub, default-path exposure, serialisation, supply chain
- **Submission Type**: Full Research Paper (ACM SIGCONF format, 8 pages main text, up to 12 pages total)

---

## Abstract

Machine learning models are increasingly published on the Web through public hubs and fetched by client applications on default execution paths. This paper investigates a fundamental provenance question for the Security and Privacy track of The Web Conference: when a derived model declares an upstream parent on a public hub, does the client fetch an artefact published by that parent, or does the derivation introduce unvetted execution hazards? We formally distinguish file presence from default-path exposure, where default client loaders fetch hazardous weight formats or dynamic configurations without explicit overrides. Evaluating a complete depth-one lineage census ($N = 48{,}247$ declared edges across 16 foundational base models) on the Hugging Face Hub, 0 of the 16 parents exhibit default-path serialisation exposure, establishing that inheritance of default-path exposure is not identified. Across child repositories, only 3.17% (95% CI: [3.01%, 3.33%]) exhibit default-path serialisation exposure, whereas 54.90% maintain legacy pickle files bypassed by default loaders. Downstream mutations outnumber repairs by 8.5x, and 11.22% of declared children launder upstream licences. Model supply chain risks on the Web arise primarily from downstream modification rather than parent inheritance.

---

## Author & Anonymous Statement

This manuscript is submitted under the mandatory double-blind review policy of The Web Conference 2027:
1. All author names, institutional affiliations, and direct identifying references have been omitted from the manuscript, supplementary files, and repository materials.
2. Self-references to prior research are cited in the third person without self-identifying attribution.
3. The underlying analysis scripts and replication materials have been scrubbed of developer usernames, hostnames, and environment paths. Automated anonymity checks (`scripts/check_anonymity.py`) pass with zero violations.
4. The research question addresses a central Web security problem: the provenance, transmission, and execution hazards of machine learning models distributed and fetched across the Web.

---

## OpenReview Intent & Author Policy Compliance

The authors formally declare their intent to complete registration on OpenReview prior to the mandatory deadlines:
- **Abstract Registration Deadline**: Sunday 18 October 2026, 23:59 AoE (Anywhere on Earth)
- **Full Paper Submission Deadline**: Sunday 25 October 2026, 23:59 AoE (Anywhere on Earth)

All declared authors comply with the WWW'27 author cap policy (no author exceeds the maximum limit of seven research-track submissions across WWW'27). The author list specified at the abstract registration deadline is final.

---

## Dual Submission Declaration

This manuscript presents original, unpublished work. It is not currently under submission, consideration, or review at any other conference, journal, or workshop. Sequential fallback options (e.g., Plan B via ICSE'28 or Plan C via FSE'28) will remain strictly dormant unless and until a formal rejection decision is issued by WWW'27.
