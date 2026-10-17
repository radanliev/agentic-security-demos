# WWW'27 Submission Checklist — Research Track

**Conference**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)  
**Track**: Research Track — Security and Privacy  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)

---

## 1. Deadlines & Schedule (Anywhere on Earth, AoE)

- [ ] **Abstract Registration Deadline**: **18 October 2026 23:59 AoE**
  - Title, author list, author order, affiliations, and abstract text must be locked in OpenReview.
  - No authors may be added, removed, or reordered after this deadline.
- [ ] **Full Paper Submission Deadline**: **25 October 2026 23:59 AoE**
  - Final PDF manuscript upload and supplementary material submission.
- [ ] **Rebuttal / Author Response Period**: 15–20 December 2026
- [ ] **Acceptance Notification**: 04 January 2027
- [ ] **Camera-Ready Version**: 31 January 2027

---

## 2. Formatting & Template Compliance

- [ ] **Document Class**: ACM primary article template using `\documentclass[sigconf,anonymous,review]{acmart}`.
- [ ] **Page Limit**:
  - Main text: Maximum **8 pages** (including all figures, tables, text, acknowledgments, but excluding references and appendices).
  - Total length: Maximum **12 pages** inclusive of references and reproducibility appendix.
- [ ] **Font & Layout**: Standard 9pt ACM font, two-column format, strictly uncompressed spacing.
- [ ] **Web Relevance**: The opening page (Section 1) clearly establishes Web significance (remote HTTP tool endpoints, secret headers, and agent-web service architectures).

---

## 3. Anonymity & Double-Blind Integrity

- [ ] **Author Disclosures**: No author names, institutional affiliations, or acknowledgments in the text or PDF properties.
- [ ] **Self-Citations**: Prior publications cited in third person (e.g. "Previous work by Smith et al. demonstrated..." rather than "Our earlier work...").
- [ ] **Code Repositories**: All links point to strictly anonymised repositories with no identifying commit messages, author metadata, or institutional URLs.
- [ ] **Automated Anonymity Gate**: Validated via automated scanner (`python3 scripts/check_anonymity.py`) with 0 findings.

---

## 4. Policy Compliance & Declarations

- [ ] **Author Cap Rule**: No listed author exceeds the limit of seven (7) research-track submissions across WWW'27.
- [ ] **Dual Submission**: The manuscript is original, unpublished work not submitted elsewhere. Fallbacks (Plan B: IMC'27 / Plan C: AsiaCCS'28) remain strictly dormant until formal rejection.
- [ ] **Conflict of Interest (COI)**: Institutional domain and individual co-authorship / supervisor conflicts fully declared in OpenReview.
- [ ] **Generative AI Disclosure**: Compliant with ACM Policy on Authorship and Generative AI (tools used solely for editorial refinement; authors retain full intellectual accountability).
- [ ] **Reproducibility**: Artifact and reproducibility protocol clearly documented in the appendix.
