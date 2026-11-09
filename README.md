<p align="center">
  <img src="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/assets/logo.svg" alt="Agentic Security Demos Logo" width="200">
</p>

<h1 align="center">Agentic AI Security Demos</h1>
<p align="center">
  <strong>A curated collection of 60 reproducible teaching demonstrations for agentic AI security, distilled from research targeting top-tier venues (SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, ICML, ICLR, AAAI, IJCAI, ACL, ICSE, WWW, EuroS&P, PoPETs, DSN, CSF, ACNS, Black Hat, DEF CON, TIFS, TDSC, TOPS, CSUR, COMST, TPAMI, TMLR, Nature MI, Journal of Cybersecurity, IEEE S&P Magazine, Scientific Data, CACM, TSE, FAccT). All scenarios, numbers and verdicts here are synthetic coursework — they describe no real publication.</strong>
</p>

> 🐣 **Padawan-practice notice (read before citing).** These are teaching demos for agentic AI security — training missions for the classroom, not Jedi trials. Like Padawan exercises, each demo **may or may not be converted into a full paper**, and any paper **may or may not be accepted** at its listed venue. The venue column names the *training ground* that inspired the exercise, never a publication claim. No preprints, no datasets deposited, no reviewer verdicts — just lightsabers set to stun (synthetic fixtures, offline only).

<p align="center">
  <a href="https://github.com/radanliev/agentic-security-demos/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/radanliev/agentic-security-demos/ci.yml?branch=main&label=Build&style=flat-square" alt="Build Status"></a>
  <a href="https://pypi.org/project/agentic-security-demos/"><img src="https://img.shields.io/pypi/v/agentic-security-demos?style=flat-square&label=PyPI" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/agentic-security-demos/"><img src="https://img.shields.io/pypi/pyversions/agentic-security-demos?style=flat-square" alt="Python Versions"></a>
  <a href="https://github.com/radanliev/agentic-security-demos/blob/main/LICENSE"><img src="https://img.shields.io/github/license/radanliev/agentic-security-demos?style=flat-square" alt="License"></a>
  <a href="https://github.com/radanliev/agentic-security-demos/stargazers"><img src="https://img.shields.io/github/stars/radanliev/agentic-security-demos?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/radanliev/agentic-security-demos/issues"><img src="https://img.shields.io/github/issues/radanliev/agentic-security-demos?style=flat-square" alt="Issues"></a>
</p>

<p align="center">
  <a href="#-demos">Demos</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-reproducibility">Reproducibility</a> •
  <a href="#-venues">Venues</a> •
  <a href="#-citation">Citation</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

---

## 🎯 Demos

| # | Demo | Focus | Status |
|---|------|-------|--------|
| 01 | **Blind Verification** | Cryptographic verification of agent outputs without trusted execution environments | 🟢 [ACM TOSEM](https://dl.acm.org/journal/tosem) |
| 02 | **Supply Chain AIBOM Drift** | AI Bill of Materials tracking & drift detection across model updates | 🟢 [EMSE](https://link.springer.com/journal/10664) |
| 03 | **Eval Design Invariants** | Statistically rigorous evaluation frameworks with invariant guarantees | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 04 | **Prompt Injection & Tool Authority** | Capability-based authority mediation for tool-using agents | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 05 | **Evidence Release Assurance** | Cryptographic evidence chains for agent accountability | 🟢 [TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 06 | **Network Recon** | eBPF-backed network reconnaissance with formal admission control | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 07 | **Malware Triage** | Statistical reconstruction of malware triage decisions | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 08 | **File Inclusion** | Provenance-tracked file inclusion for agent workflows | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 09 | **MITM Interception** | Ephemeral buffer interception for credential extraction detection | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 10 | **Vulnerability Assessment** | Cross-vendor vulnerability scanning with authoritative taxonomy | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 11 | **Degenerate Reporting** | Meta-science audit: evaluations that cannot rule out do-nothing policies | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 12 | **Provenance-Bound Authorization** | Provenance-aware authorization for untrusted calendar content | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 13 | **Typed Commitments & Coverage Cues** | Wrong coverage cues and agreement-gate failures in LLM assessors | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 14 | **Conformal Action Gating** | Distribution-free risk control for tool execution and how it fails under benchmark shift | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 15 | **Hijack Probes** | Hidden-state signatures of instruction hijack in open-weight agents | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 16 | **Infection Spread** | Epidemic dynamics of prompt-injection propagation in multi-agent systems | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 17 | **Report Fidelity** | Claims-versus-logs fidelity of coding agents | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 18 | **Cross-lingual Gap** | Cross-lingual transfer of injections and the detector language gap | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 19 | **Lineage Risk** | Inherited risk along fine-tune lineages on the model hub | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 20 | **Agent Web Census** | Agent-facing files and in-the-wild injections across the web | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 21 | **MCP Ecosystem Census** | Tool-poisoning exposure, rug-pull dynamics and capability surface across 36k MCP servers (toy census) | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 22 | **Memory Leakage** | Contextual-integrity leakage via agent memory stores | 🟠 [PoPETs](https://petsymposium.org/cfp27.php) |
| 23 | **Fault Injection** | Dependability of agent pipelines under pipeline faults | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 24 | **Delegation Checks** | Authorization and agent-to-agent delegation properties | 🟡 [CSF](https://csf2027.ieee-security.org/cfp.html) |
| 25 | **Attestation Verifier** | Install-time provenance verification for agent supply chains | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 26 | **Sandbox Probes** | Agent sandbox isolation and exfiltration controls | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 27 | **CI Trigger Scan** | Injection surface of coding agents wired to CI | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 28 | **Memory Poisoning** | Persistent memory poisoning and the MemScope auditor toy | 🟢 [WWW](https://www2027.thewebconf.org/demos/) |
| 29 | **Provenance Graphs** | Tamper-evident provenance for post-incident reconstruction | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 30 | **Default Configs** | Insecure defaults in self-hosted LLM stacks | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 31 | **Declaration Gap** | MCP registry declared-versus-exercised authority in agent integrations | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 32 | **Reproducibility Audit** | Artefact audit of the agent-security literature | 🟠 [AsiaCCS SoK](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 33 | **Protocol Coverage** | Agent protocol element × threat coverage map | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 34 | **Visual Injection** | Typographic injection against vision-language agents | 🟠 [CVPR](https://cvpr.thecvf.com/Conferences/2027/CallForPapers) |
| 35 | **Scaling Meta-regression** | Agent misbehaviour versus scale across benchmarks | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 36 | **Card Debt** | Documentation debt across open model cards | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 37 | **Detector Cost** | Injection-detector comparison with false-positive cost | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 38 | **Assurance Claims** | System-card assurance claims versus obligations | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 39 | **Incident Taxonomy** | Agentic-AI threat taxonomy for practitioners | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 40 | **Corpus Union** | License-audited unified agentic-security corpus | 🔵 [Sci Data](https://www.nature.com/sdata/) |
| 41 | **Ten Invariants** | Security invariants checklist synthesis | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 42 | **Patch Lifecycle** | Vulnerability lifecycle and patch adoption lag | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 43 | **Terms Coding** | Platform terms accountability allocation | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 44 | **Toolflow Taint** | Cross-tool dataflow integrity tracking | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 45 | **Exact Nulls for Localisation Claims** | Exact hypergeometric significance for localisation claims, ratio-to-null transfer failures, second corpus, and design-limit corollary (`radanliev/demo-45-localisation-nulls`, private; available on request) | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 46 | **Embedding-swap cosine shift** | `1 - cosine` on two synthetic vectors, compared with the frozen simulated-study mean 0.1222 (`radanliev/demo-46-simulated-embedding-drift-aibom`, private) | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 47 | **Pre-reveal Seal** | Hash a localisation commitment before the answer key opens; a post-seal edit is a mismatch (`demo-47-blind-verification-eval-sais`, private; available on request) | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 48 | **OAuth Over-privilege** | Scope creep: OAuth scope over-privilege in agent integrations (`demo-48-scope-creep-oauth-overprivilege-tops`, private; available on request) | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 49 | **Tier Fallback** | Authority invariance when an orchestrator changes model tier mid-task | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 50 | **Budget Delegation** | Token and cost budgets conserved across a multi-agent delegation tree | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 51 | **Guardrail Equity** | Accessibility-related false-positive disparity in input guardrails | 🟡 [USENIX Sec C2](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) |
| 52 | **Simulation V&V** | Held-out and contamination-probe checks for toy cohort simulators | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 53 | **Human Validation** | Sampled validation of agent outputs with planted errors | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 54 | **Stress Transfer** | A detector that passes in-distribution stress items fails under shift | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 55 | **Scaffolding Retention** | Analytic power for an immediate versus residual two-arm contrast | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 56 | **Learning Meta-analysis** | Inverse-variance fixed-effect summary of synthetic study rows | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 57 | **Governance Corpus** | Codebook validation and rater agreement on synthetic HE policy excerpts | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 58 | **Work Exposure** | Task-level exposure and an agentic-action share for synthetic HE roles | 🟡 [IJCAI](https://2027.ijcai.org/ijcai-2027-call-for-papers-main-track/) |
| 59 | **Foresight Delphi** | Median, IQR and consensus on synthetic ratings bound to a briefing hash | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 60 | **EngBio Battery** | Score three synthetic analysis tasks against predeclared references | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |

Each demo is a **self-contained, reproducible research artifact** with:
- 📦 Frozen dependencies & environment specifications
- 📊 Pre-computed evidence packages (JSON)
- 🧪 Comprehensive test suites (≥90% coverage)
- 📄 Venue-aligned documentation & claim ledgers
- 🔬 Statistical validation scripts

---

## ⚙️ Installation

```bash
git clone https://github.com/radanliev/agentic-security-demos.git
cd agentic-security-demos
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Run every demo's test suite
make test

# Run one demo's suite (folders demo-01 … demo-60)
make test DEMO=01
```

---

## 🚀 Quick Start

All demos run offline from the repository root — no API keys, no network.
Each demo folder also has step-by-step `INSTRUCTIONS.md` with expected outputs.

```bash
# Run a teaching demo (folders demo-01 … demo-60)
make demo DEMO=01   # Blind Verification
make demo DEMO=04   # Prompt Injection Authority
make demo DEMO=07   # Malware Triage
make demo DEMO=13   # Typed Commitments & Coverage Cues
make demo DEMO=14   # Conformal Action Gating (ICML toy)
make demo DEMO=21   # MCP Ecosystem Census (EuroS&P toy)
make demo DEMO=28   # Memory Poisoning (DEF CON toy)
make demo DEMO=44   # Toolflow Taint (CCS toy)
make demo DEMO=45   # Exact Nulls for Localisation Claims (SaTML toy)
make demo DEMO=46   # Embedding-swap cosine shift
make demo DEMO=47   # Pre-reveal Seal (USENIX SAIS'27 toy)

# Run a demo's test suite
make test DEMO=01

# Run every demo sequentially
make all-demos

# Check offline-safety constraints (no network imports, no credentials)
make verify-safety
```

### 30-second wiring check

```bash
make help
```

Expected output: the root command list (`make setup`, `make test DEMO=01`,
`make demo DEMO=01`, `make verify-safety`, `make all-demos`).

---

## 🔬 Reproducibility

All demos follow the **Agentic Security Reproducibility Standard**:

| Guarantee | Mechanism |
|-----------|-----------|
| **Environment Freeze** | `requirements.lock` + `conda-lock.yml` + Docker images |
| **Evidence Immutability** | SHA-256 sealed reference outputs in each demo's `results/` (🌟 Episode VI sealed Holocron — Zenodo deposit only on acceptance) |
| **Statistical Rigor** | Pre-registered analysis plans with p-value correction |
| **Compute Transparency** | GPU-hours logged; CPU fallback documented |
| **Adversarial Robustness** | Seeded RNG; deterministic attack ordering |

### Reproducibility Checklist
- [ ] Clone repo at tagged release
- [ ] Install exact dependencies: `pip install -r requirements.lock`
- [ ] Use the fixtures and reference outputs in each demo's `results/` (no external download needed)
- [ ] Run: `agentic-security-demos reproduce --all`
- [ ] Compare outputs to `results/reference/`

---

## 🏛️ Venues & Publications

> Venue abbreviation links to the conference page; the deadline line under it links to the
> submission portal (abstract + full-paper dates). **A** is the first choice; **B** / **C**
> activate only after the previous option's decision — the same work is never under review
> in two places at once.
>
> **EuroS&P 2027 cap:** at most 7 papers per author ([CFP](https://eurosp2027.ieee-security.org/cfp.html)); 7 demos are allocated (07, 10, 11, 12, 13, 17, 44). Demo 16 no longer uses DSN or EuroS&P as Option A (DSN is not a security top-10 venue; the EuroS&P cap is full); it now uses AsiaCCS 2027 Round 2. Caps are per venue: IEEE S&P allows 6 per author per cycle (6 planned for Cycle 2), USENIX Security 7 per cycle, WWW 7 per submission type; the EuroS&P cap is not shared with them, but the same paper cannot be under review at two venues at once.
>
> **Option A rule (9 November 2026):** A is the nearest real deadline at a world-leading top-5/top-10 conference that fits the page length; B and C are later top-5/top-10 venues (a top journal may be B or C) whose deadlines fall after the previous option's official notification. Notification dates checked on the official CFPs on 9 November 2026: AsiaCCS R2 31 March 2027; EuroS&P 18 March 2027; S&P Cycle 2 acceptance 5 March 2027; USENIX Security Cycle 2 6 May 2027; CSF Winter 5 April 2027; IJCAI 21 April 2027; PoPETs Issue 3 1 February 2027. USENIX Security 2027 Cycle 2 (26 January) and CSF 2027 Winter (28 January) therefore cannot follow AsiaCCS R2, EuroS&P, S&P Cycle 2 or IJCAI. DSN, ACNS and USENIX SAIS are not used as Option A. **IJCAI 2027** is reserved as demo 58's primary paper (Primary Paper Initiative). **Demo 40 exception:** Scientific Data remains Option A because it is a dataset paper with an existing submission pack, and its data stays as-is.

| Demo | Option A | Option B | Option C |
|:---:|---|---|---|
| 01 | 🟢 [ACM TOSEM](https://dl.acm.org/journal/tosem) | 🔵 [EMSE](https://link.springer.com/journal/10664) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 02 | 🟢 [EMSE](https://link.springer.com/journal/10664) | 🔵 [IEEE TSE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | 🔵 [MSR](https://www.msrconf.org/) |
| 03 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [NeurIPS 2027 (call unpublished)](https://neurips.cc/) |
| 04 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) |
| 05 | 🟢 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | — | — |
| 06 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) |
| 07 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [RAID 2027 (call unpublished)](https://dl.acm.org/conference/raid) | 🔵 [ACSAC](https://www.acsac.org/) / [ESORICS](https://conf.laas.fr/esorics) |
| 08 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ESORICS C2](https://conf.laas.fr/esorics) | 🔵 [RAID](https://dl.acm.org/conference/raid) |
| 09 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [ESORICS](https://conf.laas.fr/esorics) | 🔵 [RAID](https://dl.acm.org/conference/raid) / [ACSAC](https://www.acsac.org/) |
| 10 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [CCS](https://www.sigsac.org/ccs/CCS2027/) | 🔵 [ACSAC](https://www.acsac.org/) / [RAID](https://dl.acm.org/conference/raid) |
| 11 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [RAID 2027 (call unpublished)](https://dl.acm.org/conference/raid) | 🔵 [ESORICS](https://conf.laas.fr/esorics) / [ACSAC](https://www.acsac.org/) |
| 12 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [CCS](https://www.sigsac.org/ccs/CCS2027/) | 🔵 [NDSS](https://www.ndss-symposium.org/) |
| 13 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) |
| 14 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [NeurIPS 2027 (call unpublished)](https://neurips.cc/) |
| 15 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [ICLR 2028 (call unpublished)](https://iclr.cc/) |
| 16 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 17 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [AAMAS 2028 (call unpublished)](https://www.ifaamas.org/) |
| 18 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [ACL (ARR)](https://aclrollingreview.org/) | 🔵 [EMNLP](https://aclanthology.org/venues/emnlp/) |
| 19 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [ICSE](https://www.icse-conferences.org/)<br>🔵 [abs ~23 Jun 2027](https://www.icse-conferences.org/) | 🔵 [FSE](https://www.esec-fse.org/) |
| 20 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🟠 [WWW short](https://www2027.thewebconf.org/research-track-papers) / [IMC](https://conferences.sigcomm.org/imc/)<br>🟠 [16 Nov](https://www2027.thewebconf.org/research-track-papers) | — |
| 21 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [IMC](https://conferences.sigcomm.org/imc/) | 🔵 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/) |
| 22 | 🟠 [PoPETs](https://petsymposium.org/2027)<br>🟠 [Issue 3: 30 Nov](https://petsymposium.org/cfp27.php) | 🟡 [PoPETs Issue 4](https://petsymposium.org/2027)<br>🟡 [28 Feb](https://petsymposium.org/cfp27.php) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) |
| 23 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 24 | 🟡 [CSF Winter](https://csf2027.ieee-security.org/)<br>🟡 [papers 28 Jan](https://csf2027.ieee-security.org/cfp.html) | 🔵 [ESORICS C2](https://conf.laas.fr/esorics) / [CCS](https://www.sigsac.org/ccs/CCS2027/) | — |
| 25 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) |
| 26 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) |
| 27 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [Black Hat / Arsenal](https://www.blackhat.com/) | 🔵 [DEF CON Demo Labs](https://www.defcon.org/) |
| 28 | 🟢 [WWW demo track](https://www2027.thewebconf.org/demos/) | 🔵 [DEF CON](https://www.defcon.org/)<br>🔵 [~1 May 2027](https://www.defcon.org/) | 🔵 [Black Hat Arsenal](https://www.blackhat.com/) |
| 29 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 30 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | 🔵 [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) |
| 31 | 🟢 [FAccT](https://facctconference.org/) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 32 | 🟠 [AsiaCCS R2 SoK](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM CSUR](https://dl.acm.org/journal/csur) | 🔵 [IEEE COMST](https://www.comsoc.org/publications/journals/ieee-comst) |
| 33 | 🟠 [IEEE S&P C2 SoK](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · SoK papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [IEEE COMST](https://www.comsoc.org/publications/journals/ieee-comst) | 🔵 [Proc. IEEE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=5) |
| 34 | 🟠 [CVPR](https://cvpr.thecvf.com/Conferences/2027/CallForPapers)<br>🟠 [enroll 10 Nov · papers 16 Nov](https://cvpr.thecvf.com/Conferences/2027/Dates) | 🔵 [IEEE TPAMI](https://www.computer.org/csdl/journal/tp) | 🔵 [NeurIPS 2027 (call unpublished)](https://neurips.cc/) |
| 35 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [JMLR](https://jmlr.org/) |
| 36 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [Nature MI](https://www.nature.com/natmachintell/) | 🔵 [Patterns](https://www.cell.com/patterns) |
| 37 | 🟢 [FAccT](https://facctconference.org/) | 🔵 [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 38 | 🟢 [FAccT](https://facctconference.org/) | 🔵 [J. Cybersecurity](https://academic.oup.com/cybersecurity) | 🔵 [ACM JRC](https://dl.acm.org/journal/jrc) |
| 39 | 🟢 [FAccT](https://facctconference.org/) | 🔵 [S&P Magazine](https://www.computer.org/csdl/magazine/sp) | 🔵 [CACM Practice](https://cacm.acm.org/) |
| 40 | 🔵 [Scientific Data](https://www.nature.com/sdata/) | 🔵 [Data in Brief](https://www.sciencedirect.com/journal/data-in-brief) / [NeurIPS D&B](https://neurips.cc/) / [DMLR](https://data.mlr.press) | — |
| 41 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [CACM](https://cacm.acm.org/) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) |
| 42 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [IEEE TSE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) |
| 43 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [AIES](https://www.aies-conference.com/) | 🔵 [FAccT](https://facctconference.org/) |
| 44 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [NDSS (next cycle)](https://www.ndss-symposium.org/) | 🔵 [CCS](https://www.sigsac.org/ccs/CCS2027/) |
| 45 | 🟢 [FAccT](https://facctconference.org/) | 🟡 [USENIX Sec C2](https://www.usenix.org/conference/usenixsecurity27)<br>🟡 [papers 26 Jan (reg 19 Jan)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 46 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 47 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 48 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) |
| 49 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) / [CSF 2028 (unconfirmed)](https://csf2027.ieee-security.org/cfp.html) |
| 50 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) / [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) |
| 51 | 🟡 [USENIX Sec C2](https://www.usenix.org/conference/usenixsecurity27)<br>🟡 [papers 26 Jan (reg 19 Jan)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [FAccT 2028 (call unpublished)](https://facctconference.org/) |
| 52 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [AAMAS 2028 (call unpublished)](https://www.ifaamas.org/) |
| 53 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [ICML 2027 (call unpublished)](https://icml.cc/) / [NeurIPS 2027 (call unpublished)](https://neurips.cc/) |
| 54 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | 🔵 [CCS 2027 (dates TBD)](https://www.sigsac.org/ccs/CCS2027/cfp.html) / [SaTML 2028 (call unpublished)](https://satml.org/) |
| 55 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [FAccT 2028 (call unpublished)](https://facctconference.org/) |
| 56 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [NeurIPS 2027 (call unpublished)](https://neurips.cc/) |
| 57 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [Scientific Data](https://www.nature.com/sdata/) | 🔵 [FAccT 2028 (call unpublished)](https://facctconference.org/) |
| 58 | 🟡 [IJCAI](https://2027.ijcai.org/)<br>🟡 [abs 4 Jan · papers 11 Jan](https://2027.ijcai.org/ijcai-2027-call-for-papers-main-track/) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [FAccT 2028 (call unpublished)](https://facctconference.org/) |
| 59 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [FAccT 2028 (call unpublished)](https://facctconference.org/) |
| 60 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [SaTML 2028 (call unpublished)](https://satml.org/) / [NeurIPS 2027 (call unpublished)](https://neurips.cc/) |

---

## 📖 Citation

If you use this collection in your research, please cite:

```bibtex
@misc{agenticsecuritydemos2026,
  title={Agentic AI Security Demos: A Reproducible Teaching Collection},
  author={{Agentic Security Demos team}},
  year={2026},
  publisher={GitHub},
  journal={GitHub Repository},
  howpublished={\url{https://github.com/radanliev/agentic-security-demos}},
  note={Teaching demos with synthetic fixtures only; no preprints, no datasets deposited yet}
}
```

Individual demo citations available in each subdirectory's `CITATION.cff`.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Core Language** | Python 3.10–3.12 |
| **CLI Framework** | Click 8.x / Typer |
| **Async Runtime** | asyncio, trio |
| **Cryptography** | cryptography, pyca/cryptography |
| **eBPF** | bcc, libbpf, pyroute2 |
| **Statistics** | scipy, statsmodels, pingouin |
| **ML Frameworks** | PyTorch, transformers, vLLM |
| **Testing** | pytest, hypothesis, pytest-benchmark |
| **Packaging** | setuptools, pyproject.toml, hatch |
| **CI/CD** | GitHub Actions, pre-commit |
| **Documentation** | Sphinx, MyST-Parser, Furo theme |

---

## 🤝 Contributing

> 🌟 **Episode V – The Empire Strikes Back.** Every pull request is a trial in the snow:
> the Empire (CI) strikes back with offline tests, safety greps and schema checks. Only
> Padawans who bring evidence survive Hoth. See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- 🐛 Reporting vulnerabilities or reproducibility issues
- 💡 Proposing new demos or venues
- 🔀 Submitting pull requests (evidence-backed changes only)
- 🧪 Extending test suites
- 📝 Improving documentation

**Research Contribution Guidelines (the Jedi Code):**
1. All claims must be backed by frozen evidence packages (no Order-66 surprises)
2. Statistical claims require pre-registered analysis plans
3. New demos must target a top-tier venue with clear scope (choose your training ground)
4. Breaking changes require RFC process (consult the Council first)

---

## 📄 License

Distributed under the **MIT License** — 🌟 *a long time ago in an open-source galaxy…*
free to fork like Rebel plans, no warranty (Alderaan was also uninsured). See [LICENSE](LICENSE) for more information.

Individual demos may have additional licenses for third-party components (see `DEPENDENCIES.md`).

---

## 🙏 Acknowledgments

🌟 **The Rebel Alliance thanks:**

- **Research compute credits** — fuel for the X-wings
- **GitHub Accelerator** — the hidden Rebel base (open-source support)
- **Anonymous reviewers** at SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, ICML, ICLR, AAAI, IJCAI, ACL, ICSE, WWW, EuroS&P, PoPETs, DSN, CSF, ACNS, TIFS, TDSC, TOPS, CSUR, COMST, TPAMI, TMLR, Nature MI, Journal of Cybersecurity, Scientific Data, CACM, TSE, FAccT — the Jedi Council: wise, anonymous, occasionally striking back (Episode V)
- **Agentic AI Security community** — the Ewoks who actually help (feedback and replication)

---

<p align="center">
  <strong>Training Padawans in agentic AI security, one reproducible demo at a time — may the Force (of offline, synthetic fixtures) be with you.</strong>
</p>

<p align="center">
  <a href="https://github.com/radanliev/agentic-security-demos/stargazers">⭐ Star</a> •
  <a href="https://github.com/radanliev/agentic-security-demos/fork">🍴 Fork</a> •
  <a href="https://github.com/radanliev/agentic-security-demos/issues">🐛 Report Issue</a> •
  <a href="https://github.com/radanliev/agentic-security-demos/discussions">💬 Discuss</a>
</p>