# Submission Package: Option B — Black Hat USA 2027 (Briefings & Arsenal)

This directory contains the prepared submission package for **Plan B** of Demo 27 (`ci-trigger-scan`).

---

## Venue & Target Information

- **Venue**: Black Hat USA 2027, Mandalay Bay, Las Vegas, NV (August 2027)
- **Track**: Briefings (Application Security) / Black Hat Arsenal (Open Source Security Tools)
- **Submission Platform**: Black Hat CFP Portal (`https://www.blackhat.com/us-27/call-for-papers.html`)
- **Key Deadlines**:
  - **Briefings CFP Deadline**: **~May 2027**
  - **Arsenal CFP Deadline**: **~June 2027**
  - **Event**: **August 2027**
- **Status**: `pending`
- **Activation Trigger**: `after WWW rejection`

---

## Sequential Policy Enforcement

This package represents a sequential fallback. It remains **dormant** while Plan A is under evaluation at The Web Conference 2027 (WWW'27). It must **never** be submitted concurrently with Plan A. Activation occurs only after an explicit rejection notification from WWW'27 (scheduled for 04 January 2027), providing substantial runway before the Black Hat CFP close.

---

## Submission Package Contents

| File | Purpose | Notes |
|------|---------|-------|
| [`abstract_bhusa27.txt`](abstract_bhusa27.txt) | CFP abstract text | Concise practitioner-focused abstract highlighting vulnerability mechanics, census metrics, and tool demonstration |
| [`manuscript_bhusa27.tex`](manuscript_bhusa27.tex) | Technical whitepaper & briefing outline | Complete technical briefing structure covering the confused deputy exploit, empirical census, and tool architecture |
| [`cover_letter_bhusa27.md`](cover_letter_bhusa27.md) | Author & speaker cover letter | Details presentation format, Arsenal station plan, speaker qualifications, and sequential submission status |
| [`submission_checklist_bhusa27.md`](submission_checklist_bhusa27.md) | Pre-submission verification checklist | Verifies deadlines, demo safety requirements, CFP portal fields, and WWW'27 gate resolution |

---

## Refresh Protocol Before Submission

Prior to activating this package upon a WWW'27 rejection:
1. Verify the official rejection decision from WWW'27 on or after 04 January 2027.
2. Ingest reviewer feedback from WWW'27 to refine technical explanations and threat model boundaries.
3. Package the latest version of `ci-trigger-scan` into an easily installable Python package or Docker container for the Arsenal demo.
4. Prepare slide deck drafts adhering to the Black Hat USA template guidelines.
