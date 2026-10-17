# Submission Packages: Demo 19 (Lineage Risk)

This directory manages the sequential conference submission pipeline for **Demo 19: Lineage Risk** (*What a Client Fetches: Default-Path Exposure of Models Published on the Web*).

---

## Target Venues & Strategy Overview

In accordance with responsible academic submission policies, this project follows a strict **single-submission sequential protocol**. Only **Option A** is active; Options B and C remain dormant fallbacks to be considered only in the event of formal rejection from prior venues.

| Option | Venue | Track | Format | Key Deadlines (AoE) | Status | Activation Trigger | Directory |
|---|---|---|---|---|---|---|---|
| **A** | **The Web Conference 2027 (WWW'27)**, Dublin | Research Track: Security and Privacy | ACM SIGCONF (8 pages + refs/app up to 12 pages) | Abstract: 18 Oct 2026<br>Paper: 25 Oct 2026 | **prepared** | **Submit now** | [`Option_A_WWW27/`](Option_A_WWW27/) |
| **B** | **ICSE 2028**, 50th Int. Conf. on Software Engineering | Research Track | IEEE/ACM format (10 pages + 2 pages refs) | Abstract: ~23 Jun 2027<br>Paper: ~30 Jun 2027 | pending | After WWW'27 rejection decision | [`Option_B_ICSE28/`](Option_B_ICSE28/) |
| **C** | **FSE 2028**, ACM Int. Conf. on Foundations of Software Engineering | Research Track | ACM SIGCONF format (10 pages + refs) | Expected ~Autumn 2027 cycle | pending | After ICSE'28 rejection decision | [`Option_C_FSE28/`](Option_C_FSE28/) |

---

## Directory Structure

```
submission/
├── README.md                          # This master roadmap
├── Option_A_WWW27/                    # Primary target: WWW'27 Security and Privacy
│   ├── README.md                      # Package overview and activation guide
│   ├── abstract_abstract_www27.txt    # Registration abstract (<200 words)
│   ├── abstract_www27.txt             # Canonical abstract copy
│   ├── manuscript_www27.tex           # ACM SIGCONF manuscript shell
│   ├── cover_letter_www27.md          # Author cover letter and disclosures
│   └── submission_checklist_www27.md  # Verification checklist & deadlines
├── Option_B_ICSE28/                   # Plan B fallback: ICSE'28 Software Supply Chain
│   ├── README.md                      # Package overview and activation guide
│   ├── abstract_icse28.txt            # Software engineering framed abstract
│   ├── manuscript_icse28.tex          # IEEE/ACM format manuscript shell
│   ├── cover_letter_icse28.md         # Author cover letter
│   └── submission_checklist_icse28.md  # Verification checklist
└── Option_C_FSE28/                    # Plan C fallback: FSE'28 Foundations
    ├── README.md                      # Package overview and activation guide
    ├── abstract_fse28.txt             # Foundations framed abstract
    ├── manuscript_fse28.tex           # ACM format manuscript shell
    ├── cover_letter_fse28.md          # Author cover letter
    └── submission_checklist_fse28.md  # Verification checklist
```

---

## Sequential Policy & Conflict Prevention

- **No Concurrent Submission**: The work is not submitted to more than one refereed venue at any time.
- **Review Cycle Safety**: WWW'27 notifications are scheduled for 04 January 2027. Fallback targets (ICSE'28 in June 2027, FSE'28 in late 2027) fall well after the WWW'27 decision boundary.
- **Anonymity**: All packages strictly preserve double-blind anonymity requirements.
