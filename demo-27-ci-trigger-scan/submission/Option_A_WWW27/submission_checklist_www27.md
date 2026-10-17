# WWW'27 Submission Checklist — Research Track

**Conference**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)  
**Track**: Research Track — Web Infrastructure and Agentic Systems  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)

---

## 1. Deadlines & Schedule (Anywhere on Earth, AoE)

- [ ] **Abstract Registration Deadline**: **18 October 2026 23:59 AoE**
  - Paper title, author list, author order, affiliations, and abstract text must be registered and locked in OpenReview.
  - The author list is frozen at abstract registration; no authors may be added, removed, or reordered subsequently.
- [ ] **Full Paper Submission Deadline**: **25 October 2026 23:59 AoE**
  - Final PDF manuscript upload and optional supplementary materials.
- [ ] **Author Response / Rebuttal Period**: 15–20 December 2026
- [ ] **Acceptance Notification**: 04 January 2027
- [ ] **Camera-Ready Version Deadline**: 31 January 2027

---

## 2. Formatting & Template Compliance

- [ ] **Document Class**: ACM primary article template using `\documentclass[sigconf,anonymous,review]{acmart}`.
- [ ] **Page Budget**:
  - Main text: Maximum **8 content pages** (including all figures, tables, text, acknowledgments, but excluding references and appendices).
  - Total length: Maximum **12 pages** inclusive of references and optional reproducibility appendix.
- [ ] **Typography & Layout**: Standard ACM two-column layout, uncompressed spacing, standard margins.
- [ ] **Web Relevance Requirement**: The opening page (Section 1) clearly articulates why the research addresses Web infrastructure and Web agentic systems (delegated authority and prompt injection via public forge webhooks).

---

## 3. Anonymity & Double-Blind Integrity

- [ ] **Author Disclosures**: No author names, institutional affiliations, or acknowledgments appear in the manuscript or metadata.
- [ ] **Third-Person Citations**: All citations to prior work by the authors are written strictly in the third person.
- [ ] **Repository Anonymisation**: External links point to anonymised repositories without identifying commit logs, author emails, or institutional URLs.
- [ ] **Automated Anonymity Gate**: Validated with repo-relative checks (`python3 scripts/check_anonymity.py`) reporting 0 violations.

---

## 4. Policy Compliance & Declarations

- [ ] **Author Cap Rule**: No listed author exceeds the limit of seven (7) submissions to the WWW'27 research track.
- [ ] **Dual Submission Rule**: The manuscript contains original, unpublished work not under concurrent review elsewhere. Sequential fallbacks (Plan B / Plan C) remain dormant.
- [ ] **Conflict of Interest (COI)**: Institutional domain and personal conflicts declared in OpenReview.
- [ ] **Generative AI Policy**: Compliant with ACM Policy on Authorship and Generative AI.
- [ ] **Reproducibility**: Analysis scripts, workflow schemas, and synthetic demonstration fixtures documented for reproducibility review.
