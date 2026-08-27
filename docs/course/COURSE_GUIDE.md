# Agentic AI Security — Complete Course Guide

**A 10-module hands-on course for teaching security engineering in agentic AI systems.**

---

## 📋 Course Overview

| Attribute | Value |
|-----------|-------|
| **Format** | 10 hands-on lab modules + setup + final assessment |
| **Duration** | 12–15 hours total (self-paced) |
| **Level** | Advanced undergraduate / Master's CS |
| **Prerequisites** | Python 3.11+, basic networking, basic security concepts |
| **Safety** | 100% offline — synthetic fixtures only, zero live targets |
| **Assessment** | Lab completion + exercise portfolio + final quiz |

---

## 🎯 Course Learning Outcomes

By the end of this course, students will be able to:

1. **Explain** why post-hoc explanations cannot verify agent behavior, and implement blind-commitment oracles.
2. **Detect** drift between declared AI-BOM inventories and runtime agent capabilities using fail-closed policy gates.
3. **Design** executable evaluation invariants that catch leakage, saturation, instability, misclassification, and missing metadata.
4. **Implement** provenance tracking and capability-token mediation to defeat confused-deputy attacks.
5. **Build** cryptographically verifiable evidence pipelines (hash chains, Merkle trees, inclusion proofs) for release assurance.
6. **Recognize** indirect prompt injection in network protocol data and enforce scope-restricted reconnaissance.
7. **Perform** safe malware triage using base-rate reasoning and provenance-aware quarantine decisions — without executing samples.
8. **Distinguish** file *reading* from *authority granting* in local/remote inclusion scenarios.
9. **Apply** taint tracking and downstream action guards to intercepted traffic processing.
10. **Constrain** autonomous vulnerability scanners with scope validation, AST-based check validation, and taint-aware action policies.

---

## 🗺️ Course Map & Suggested Schedule

```
Week 1 ──┬── Module 0: Setup & Safety Orientation          (1 hour)
         └── Module 1: Blind Verification                   (1 hour)

Week 2 ──┬── Module 2: Supply Chain & AIBOM Drift           (1 hour)
         └── Module 3: Evaluation Invariants                (1.5 hours)

Week 3 ──┬── Module 4: AuthorityBound (Confused Deputy)     (1.5 hours)
         └── Module 5: Evidence-Backed Release (EVIAssure)  (1.5 hours)

Week 4 ──┬── Module 6: ReconScope (Network Recon Safety)    (1 hour)
         └── Module 7: TriageTrap (Safe Malware Triage)     (1 hour)

Week 5 ──┬── Module 8: InclusionTrap (File Inclusion)       (1.5 hours)
         ├── Module 9: InterceptBound (Traffic & Taint)     (1.5 hours)
         └── Module 10: ScanBound (Vuln Scan Control)       (1.5 hours)

Week 6 ───── Final Assessment & Portfolio Review           (2 hours)
```

**Total: ~15 hours across 6 weeks** (or 3 intensive full days)

---

## 📚 Module Dependency Graph

```
                    ┌─────────────────────┐
                    │  Module 0: Setup    │
                    │  & Safety           │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Module 1:        │ │ Module 2:        │ │ Module 6:        │
│ Blind            │ │ Supply Chain     │ │ ReconScope       │
│ Verification     │ │ AIBOM Drift      │ │ (Network)        │
│ [FOUNDATIONS]    │ │ [GOVERNANCE]     │ │ [NETWORK]        │
└────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Module 3:        │ │ Module 4:        │ │ Module 7:        │
│ Eval Invariants  │ │ AuthorityBound   │ │ TriageTrap       │
│ [METHODOLOGY]    │ │ [ACCESS CONTROL] │ │ [MALWARE]        │
└────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                    │                    │
         └────────────┬───────┴────────────────────┘
                      ▼
          ┌──────────────────────┐
          │ Module 5: EVIAssure  │
          │ [CRYPTOGRAPHY]       │
          └──────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Module 8:    │ │ Module 9:    │ │ Module 10:   │
│ InclusionTrap│ │ InterceptBound│ │ ScanBound   │
│ [FILES]      │ │ [TRAFFIC]    │ │ [SCANNING]   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       └────────────────┼────────────────┘
                        ▼
          ┌─────────────────────────┐
          │  Final Assessment       │
          └─────────────────────────┘
```

**Recommended paths:**
- **Fast track (3 days)**: 0 → 1 → 2 → 4 → 5 → 8 → 9 → 10
- **Network focus**: 0 → 1 → 6 → 7 → 9 → 10
- **Governance focus**: 0 → 2 → 3 → 5 → 10

---

## 🛡️ Safety Contract (Must Sign Before Module 1)

Before starting, students must read and acknowledge [RESPONSIBLE_USE.md](../../RESPONSIBLE_USE.md):

> I understand that:
> - All demos run **100% offline** against synthetic fixtures
> - I must **never** point any tool at public IPs, domains, or real services
> - I must **never** use real credentials, API keys, or private keys
> - I must **never** execute unknown binaries or real malware
> - Teaching results are **demonstrations**, not validated research claims
> - Violations may violate computer fraud laws (e.g., CFAA) and course policy

**Signature**: ______________________ **Date**: __________

---

## 📊 Assessment Structure

| Component | Weight | Description |
|-----------|--------|-------------|
| **Lab Completion** | 40% | All 10 modules run successfully with recorded results |
| **Exercise Portfolio** | 35% | Beginner (all) + Standard (all) + Extension (≥5) exercises |
| **Final Quiz** | 15% | 25 questions covering all learning outcomes |
| **Reflection Report** | 10% | 2-page analysis: which defense failed hardest to implement and why |

### Grading Rubric (per lab)

| Criterion | Pass | Good | Excellent |
|-----------|------|------|-----------|
| Demo runs | Output produced | Correct output | Correct + interpreted |
| Exercises | Beginner done | + Standard done | + Extension done |
| Understanding | Followed steps | Can explain why | Can teach others |
| Results recorded | JSON saved | Metadata complete | Reproducible by peer |

---

## 📁 Deliverables Per Module

Students must submit per module:

1. **`results/` directory** — JSON outputs from `make demo`
2. **`LAB_NOTES.md`** — Answers to 3 reflection questions (in each lab guide)
3. **Exercise solutions** — Committed code in `student/` or `solutions/`
4. **Reproducibility record** — Seed, commit, environment, command

---

## 🔧 Instructor Setup

```bash
# 1. Clone and verify
git clone https://github.com/radanliev/agentic-security-demos.git
cd agentic-security-demos
make setup && make test   # Must end with "=== All tests passed ===" (293 passed, 1 xfailed)

# 2. Verify safety gates
make verify-safety

# 3. (Optional) Prepare instructor-only solutions
# solutions/ directories are gitignored in the public repo
```

**Classroom requirements:**
- Each student: laptop with Python 3.11+, git, make
- No internet needed during labs (fully offline after clone)
- ~500 MB disk per student

---

## 📖 Module Index

| Module | Lab Guide | Demo Directory | Core Concept |
|--------|-----------|----------------|--------------|
| 0 | [Setup & Safety](lab-00-setup.md) | — | Environment + safety contract |
| 1 | [Blind Verification](lab-01-blind-verification.md) | `demo-01-blind-verification/` | Commit-before-test oracles |
| 2 | [Supply Chain & AIBOM](lab-02-supply-chain-aibom.md) | `demo-02-supply-chain-aibom/` | Drift detection & policy gates |
| 3 | [Evaluation Invariants](lab-03-eval-invariants.md) | `demo-03-eval-invariants/` | 5 executable eval checks |
| 4 | [AuthorityBound](lab-04-authoritybound.md) | `demo-04-authoritybound/` | Confused deputy & provenance |
| 5 | [EVIAssure](lab-05-eviassure.md) | `demo-05-eviassure/` | Hash chains & Merkle proofs |
| 6 | [ReconScope](lab-06-reconscope.md) | `demo-06-reconscope/` | Injection in protocol data |
| 7 | [TriageTrap](lab-07-triagetrap.md) | `demo-07-triagetrap/` | Base-rate-aware triage |
| 8 | [InclusionTrap](lab-08-inclusiontrap.md) | `demo-08-inclusiontrap/` | Reading ≠ authority |
| 9 | [InterceptBound](lab-09-interceptbound.md) | `demo-09-interceptbound/` | Taint tracking & action guards |
| 10 | [ScanBound](lab-10-scanbound.md) | `demo-10-scanbound/` | Scope-bound vulnerability scanning |
| Final | [Assessment](lab-11-final-assessment.md) | — | Quiz + portfolio + reflection |

---

*Course version 1.0 | Aligned with repository v0.1.0 | 294 tests, seed=42, fully offline*
