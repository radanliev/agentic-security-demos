# Submission Package: Option A — The Web Conference 2027 (WWW'27)

This directory contains the prepared submission package for **Plan A** of Demo 20 (`agent-web-census`).

---

## Venue & Target Information

- **Venue**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)
- **Track**: Research Track — Web Infrastructure and Agentic Systems
- **Submission Platform**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)
- **Key Deadlines (AoE, UTC-12)**:
  - **Abstract Registration**: **18 October 2026 23:59 AoE**
  - **Full Paper Submission**: **25 October 2026 23:59 AoE**
  - **Rebuttal Period**: 15–20 December 2026
  - **Notification**: 04 January 2027
  - **Camera-Ready**: 31 January 2027
- **Status**: `prepared`
- **Activation Trigger**: `submit now`

---

## Submission Package Contents

| File | Purpose | Notes |
|------|---------|-------|
| [`abstract_abstract_www27.txt`](abstract_abstract_www27.txt) | Portal abstract text | Draft abstract, under 200 words, formatted for OpenReview portal registration |
| [`manuscript_www27.tex`](manuscript_www27.tex) | ACM SIGCONF manuscript shell | Anonymous double-blind format; template to be refreshed prior to compilation |
| [`cover_letter_www27.md`](cover_letter_www27.md) | Author cover letter | Outlines paper details, track, abstract, keywords, anonymity, and OpenReview intent |
| [`submission_checklist_www27.md`](submission_checklist_www27.md) | Pre-submission verification checklist | Covers deadlines, ACM SIGCONF format, page budget, anonymity, and author cap |

---

## Refresh Protocol Before Final Submission

Documents in this directory are templates and shells. Prior to final portal submission:
1. Re-sync the manuscript text and macros from the primary research repository (`demo-20-agent-facing-web-commoncrawl-www`).
2. Verify word count and character limits on OpenReview for abstract registration.
3. Validate double-blind compliance and anonymity gates (`python3 scripts/check_anonymity.py`).
4. Ensure page budget adheres to the 8-page main body limit (12 pages total).
