<p align="center">
  <img src="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/assets/logo.svg" alt="Agentic Security Demos Logo" width="200">
</p>

<h1 align="center">Agentic AI Security Demos</h1>
<p align="center">
  <strong>A curated collection of 48 reproducible teaching demonstrations for agentic AI security, distilled from research targeting top-tier venues (SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, ICML, ICLR, AAAI, IJCAI, ACL, ICSE, WWW, EuroS&P, PoPETs, DSN, CSF, ACNS, Black Hat, DEF CON, TIFS, TDSC, TOPS, CSUR, COMST, TPAMI, TMLR, Nature MI, Journal of Cybersecurity, IEEE S&P Magazine, Scientific Data, CACM, TSE, FAccT). All scenarios, numbers and verdicts here are synthetic coursework — they describe no real publication.</strong>
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
| 03 | **Eval Design Invariants** | Statistically rigorous evaluation frameworks with invariant guarantees | 🟡 [IJCAI](https://2027.ijcai.org/ijcai-2027-call-for-papers-main-track/) |
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
| 14 | **Conformal Action Gating** | Distribution-free risk control for tool execution and how it fails under benchmark shift | 🟠 [DSN](https://dsn2027-berlin.github.io/call-for-contributions) |
| 15 | **Hijack Probes** | Hidden-state signatures of instruction hijack in open-weight agents | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 16 | **Infection Spread** | Epidemic dynamics of prompt-injection propagation in multi-agent systems | 🟠 [DSN](https://dsn2027-berlin.github.io/call-for-contributions) |
| 17 | **Report Fidelity** | Claims-versus-logs fidelity of coding agents | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 18 | **Cross-lingual Gap** | Cross-lingual transfer of injections and the detector language gap | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 19 | **Lineage Risk** | Inherited risk along fine-tune lineages on the model hub | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 20 | **Agent Web Census** | Agent-facing files and in-the-wild injections across the web | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 21 | **MCP Ecosystem Census** | Tool-poisoning exposure, rug-pull dynamics and capability surface across 36k MCP servers (toy census) | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 22 | **Memory Leakage** | Contextual-integrity leakage via agent memory stores | 🟠 [PoPETs](https://petsymposium.org/cfp27.php) |
| 23 | **Fault Injection** | Dependability of agent pipelines under pipeline faults | 🟠 [DSN](https://dsn2027-berlin.github.io/call-for-contributions) |
| 24 | **Delegation Checks** | Authorization and agent-to-agent delegation properties | 🟡 [CSF](https://csf2027.ieee-security.org/cfp.html) |
| 25 | **Attestation Verifier** | Install-time provenance verification for agent supply chains | 🟡 [ACNS](https://acns2027.isg.rhul.ac.uk/calls/papers) |
| 26 | **Sandbox Probes** | Agent sandbox isolation and exfiltration controls | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 27 | **CI Trigger Scan** | Injection surface of coding agents wired to CI | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 28 | **Memory Poisoning** | Persistent memory poisoning and the MemScope auditor toy | 🟢 [WWW](https://www2027.thewebconf.org/demos/) |
| 29 | **Provenance Graphs** | Tamper-evident provenance for post-incident reconstruction | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 30 | **Default Configs** | Insecure defaults in self-hosted LLM stacks | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 31 | **Declaration Gap** | MCP registry declared-versus-exercised authority in agent integrations | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 32 | **Reproducibility Audit** | Artefact audit of the agent-security literature | 🔵 [CSUR](https://dl.acm.org/journal/csur) |
| 33 | **Protocol Coverage** | Agent protocol element × threat coverage map | 🟠 [S&P](https://sp2027.ieee-security.org/cfpapers.html) |
| 34 | **Visual Injection** | Typographic injection against vision-language agents | 🔵 [TPAMI](https://www.computer.org/csdl/journal/tp) |
| 35 | **Scaling Meta-regression** | Agent misbehaviour versus scale across benchmarks | 🔵 [TMLR](https://jmlr.org/tmlr/) |
| 36 | **Card Debt** | Documentation debt across open model cards | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 37 | **Detector Cost** | Injection-detector comparison with false-positive cost | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 38 | **Assurance Claims** | System-card assurance claims versus obligations | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 39 | **Incident Taxonomy** | Agentic-AI threat taxonomy for practitioners | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 40 | **Corpus Union** | License-audited unified agentic-security corpus | 🔵 [Sci Data](https://www.nature.com/sdata/) |
| 41 | **Ten Invariants** | Security invariants checklist synthesis | 🔵 [CACM](https://cacm.acm.org/) |
| 42 | **Patch Lifecycle** | Vulnerability lifecycle and patch adoption lag | 🔵 [TSE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) |
| 43 | **Terms Coding** | Platform terms accountability allocation | 🟢 [WWW](https://www2027.thewebconf.org/research-track-papers) |
| 44 | **Toolflow Taint** | Cross-tool dataflow integrity tracking | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/cfp.html) |
| 45 | **Exact Nulls for Localisation Claims** | Exact hypergeometric significance for localisation claims, ratio-to-null transfer failures, second corpus, and design-limit corollary (`radanliev/demo-45-localisation-nulls`, private; available on request) | 🟢 [FAccT](https://facctconference.org/2027/cfp.html) |
| 46 | **Embedding-swap cosine shift** | `1 - cosine` on two synthetic vectors, compared with the frozen simulated-study mean 0.1222 (`radanliev/demo-46-simulated-embedding-drift-aibom`, private) | 🟠 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) |
| 47 | **Pre-reveal Seal** | Hash a localisation commitment before the answer key opens; a post-seal edit is a mismatch (`demo-47-blind-verification-eval-sais`, private; available on request) | 🟡 [SAIS](https://www.usenix.org/conference/sais27/call-for-papers) |
| 48 | **OAuth Over-privilege** | Scope creep: OAuth scope over-privilege in agent integrations (`demo-48-scope-creep-oauth-overprivilege-tops`, private; available on request) | 🟡 [TOPS](https://dl.acm.org/journal/tops) |

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

# Run one demo's suite (folders demo-01 … demo-48)
make test DEMO=01
```

---

## 🚀 Quick Start

All demos run offline from the repository root — no API keys, no network.
Each demo folder also has step-by-step `INSTRUCTIONS.md` with expected outputs.

```bash
# Run a teaching demo (folders demo-01 … demo-48)
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
> **EuroS&P 2027 cap:** at most 7 papers per author ([CFP](https://eurosp2027.ieee-security.org/cfp.html)); 7 demos are allocated (07, 10, 11, 12, 13, 17, 44). IEEE S&P C2 demos list EuroS&P only as an after-rejection Plan B. Demo 16 fits EuroS&P's scope but is first reserve (core multi-agent results still pending). Caps are per venue: IEEE S&P allows 6 per author per cycle (6 planned for Cycle 2), USENIX Security 7 per cycle, WWW 7 per submission type; the EuroS&P cap is not shared with them, but the same paper cannot be under review at two venues at once.

| Demo | Option A | Option B | Option C |
|:---:|---|---|---|
| 01 | 🟢 [ACM TOSEM](https://dl.acm.org/journal/tosem) | 🔵 [EMSE](https://link.springer.com/journal/10664) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 02 | 🟢 [EMSE](https://link.springer.com/journal/10664) | 🔵 [IEEE TSE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | 🔵 [MSR](https://www.msrconf.org/) |
| 03 | 🟡 [IJCAI](https://2027.ijcai.org/)<br>🟡 [abs 4 Jan · papers 11 Jan](https://2027.ijcai.org/ijcai-2027-call-for-papers-main-track/) | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [NeurIPS E&D (2027 call unconfirmed)](https://neurips.cc/) |
| 04 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [EuroS&P (if rejected)](https://eurosp2027.ieee-security.org/) / [USENIX Sec](https://www.usenix.org/conference/usenixsecurity27) | 🔵 [CCS Cycle B](https://www.sigsac.org/ccs/CCS2027/) |
| 05 | 🟢 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | — | — |
| 06 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | 🔵 [DIMVA](https://dimva.org/) / [USENIX Sec](https://www.usenix.org/conference/usenixsecurity27) |
| 07 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [RAID](https://dl.acm.org/conference/raid) / [DIMVA](https://dimva.org/) | 🔵 [ACSAC](https://www.acsac.org/) / [ESORICS](https://conf.laas.fr/esorics) |
| 08 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ESORICS C2](https://conf.laas.fr/esorics) | 🔵 [RAID](https://dl.acm.org/conference/raid) |
| 09 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [EuroS&P (if rejected)](https://eurosp2027.ieee-security.org/) / [ESORICS](https://conf.laas.fr/esorics) | 🔵 [RAID](https://dl.acm.org/conference/raid) / [ACSAC](https://www.acsac.org/) |
| 10 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [USENIX Sec](https://www.usenix.org/conference/usenixsecurity27) / [CCS](https://www.sigsac.org/ccs/CCS2027/) | 🔵 [ACSAC](https://www.acsac.org/) / [RAID](https://dl.acm.org/conference/raid) |
| 11 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [RAID](https://dl.acm.org/conference/raid) / [DIMVA](https://dimva.org/) | 🔵 [ESORICS](https://conf.laas.fr/esorics) / [ACSAC](https://www.acsac.org/) |
| 12 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [USENIX Sec](https://www.usenix.org/conference/usenixsecurity27) / [CCS](https://www.sigsac.org/ccs/CCS2027/) | 🔵 [NDSS](https://www.ndss-symposium.org/) |
| 13 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [USENIX Sec](https://www.usenix.org/conference/usenixsecurity27) / [CSF](https://csf2027.ieee-security.org/) | 🔵 [CCS](https://www.sigsac.org/ccs/CCS2027/) / [NDSS](https://www.ndss-symposium.org/) |
| 14 | 🟠 [DSN](https://dsn2027-berlin.github.io/)<br>🟠 [abs 25 Nov · papers 2 Dec](https://dsn2027-berlin.github.io/call-for-contributions) | 🔵 [TMLR](https://jmlr.org/tmlr/) / [NeurIPS D&B](https://neurips.cc/) | 🔵 [ICML (2027 call unconfirmed)](https://icml.cc/) / [ICLR](https://iclr.cc/) |
| 15 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🔵 [ICML (2027 call unconfirmed)](https://icml.cc/) / [TMLR](https://jmlr.org/tmlr/) / [NeurIPS D&B](https://neurips.cc/) | 🔵 [ICLR 2028 (unconfirmed)](https://iclr.cc/) |
| 16 | 🟠 [DSN](https://dsn2027-berlin.github.io/)<br>🟠 [abs 25 Nov · papers 2 Dec](https://dsn2027-berlin.github.io/call-for-contributions) | 🔵 [EuroS&P (first reserve)](https://eurosp2027.ieee-security.org/) / [SAIS](https://www.usenix.org/conference/sais27)<br>🟡 [papers 4 Feb](https://www.usenix.org/conference/sais27/call-for-papers) | 🔵 [AAAI-28 (unconfirmed)](https://aaai.org/Conferences/AAAI) / [IJCAI](https://www.ijcai.org/) / [AAMAS](https://www.ifaamas.org/) |
| 17 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [IJCAI](https://www.ijcai.org/) / [AAAI](https://aaai.org/Conferences/AAAI) | 🔵 [AAMAS](https://www.ifaamas.org/) / [ECAI](https://ecai.eu/) / [TMLR](https://jmlr.org/tmlr/) |
| 18 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [ACL (ARR)](https://aclrollingreview.org/) | 🔵 [EMNLP](https://aclanthology.org/venues/emnlp/) |
| 19 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [ICSE](https://www.icse-conferences.org/)<br>🔵 [abs ~23 Jun 2027](https://www.icse-conferences.org/) | 🔵 [FSE](https://www.esec-fse.org/) |
| 20 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🟠 [WWW short](https://www2027.thewebconf.org/research-track-papers) / [IMC](https://conferences.sigcomm.org/imc/)<br>🟠 [16 Nov](https://www2027.thewebconf.org/research-track-papers) | — |
| 21 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [IMC](https://conferences.sigcomm.org/imc/) | 🔵 [AsiaCCS](https://asiaccs2027.cityu.edu.mo/) |
| 22 | 🟠 [PoPETs](https://petsymposium.org/2027)<br>🟠 [Issue 3: 30 Nov](https://petsymposium.org/cfp27.php) | 🟡 [PoPETs Issue 4](https://petsymposium.org/2027)<br>🟡 [28 Feb](https://petsymposium.org/cfp27.php) | 🔵 [USENIX Sec](https://www.usenix.org/conference/usenixsecurity27) |
| 23 | 🟠 [DSN](https://dsn2027-berlin.github.io/)<br>🟠 [abs 25 Nov · papers 2 Dec](https://dsn2027-berlin.github.io/call-for-contributions) | 🔵 [ISSRE](https://issre.org/) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 24 | 🟡 [CSF Winter](https://csf2027.ieee-security.org/)<br>🟡 [papers 28 Jan](https://csf2027.ieee-security.org/cfp.html) | 🔵 [ESORICS C2](https://conf.laas.fr/esorics) / [CCS](https://www.sigsac.org/ccs/CCS2027/) | — |
| 25 | 🟡 [ACNS C2](https://acns2027.isg.rhul.ac.uk/)<br>🟡 [papers 21 Jan](https://acns2027.isg.rhul.ac.uk/calls/papers) | 🔵 [ESORICS C2](https://conf.laas.fr/esorics) / [EuroS&P](https://eurosp2027.ieee-security.org/) / [AsiaCCS](https://asiaccs2027.cityu.edu.mo/) | — |
| 26 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [EuroS&P (if rejected)](https://eurosp2027.ieee-security.org/) / [ACSAC](https://www.acsac.org/)<br>🔵 [~26 May 2027](https://submit.acsac.org/) | 🔵 [DIMVA](https://dimva.org/) / [AsiaCCS](https://asiaccs2027.cityu.edu.mo/) |
| 27 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [Black Hat / Arsenal](https://www.blackhat.com/) | 🔵 [DEF CON Demo Labs](https://www.defcon.org/) |
| 28 | 🟢 [WWW demo track](https://www2027.thewebconf.org/demos/) | 🔵 [DEF CON](https://www.defcon.org/)<br>🔵 [~1 May 2027](https://www.defcon.org/) | 🔵 [Black Hat Arsenal](https://www.blackhat.com/) |
| 29 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [EuroS&P (if rejected)](https://eurosp2027.ieee-security.org/) / [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 30 | 🟠 [IEEE S&P C2](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [EuroS&P (if rejected)](https://eurosp2027.ieee-security.org/) / [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | 🔵 [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) |
| 31 | 🟢 [FAccT](https://facctconference.org/) | 🔵 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 32 | 🔵 [ACM CSUR](https://dl.acm.org/journal/csur) | 🔵 [COMST](https://www.comsoc.org/publications/journals/ieee-comst) / [DTRAP](https://dl.acm.org/journal/dtrap) / [Computers & Sec.](https://www.sciencedirect.com/journal/computers-and-security) | — |
| 33 | 🟠 [IEEE S&P C2 SoK](https://sp2027.ieee-security.org/)<br>🟠 [abs 10 Nov · SoK papers 17 Nov](https://sp2027.ieee-security.org/cfpapers.html) | 🔵 [EuroS&P (if rejected)](https://eurosp2027.ieee-security.org/) / [IEEE COMST](https://www.comsoc.org/publications/journals/ieee-comst) | 🔵 [Proc. IEEE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=5) |
| 34 | 🔵 [IEEE TPAMI](https://www.computer.org/csdl/journal/tp) | 🔵 [TNNLS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=5962385) / [TIP](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=83) / [TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | — |
| 35 | 🔵 [TMLR](https://jmlr.org/tmlr/) | 🔵 [JMLR](https://jmlr.org/) / [DMLR](https://data.mlr.press) / [ICML](https://icml.cc/) | — |
| 36 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [Nature MI](https://www.nature.com/natmachintell/) | 🔵 [Patterns](https://www.cell.com/patterns) |
| 37 | 🟢 [FAccT](https://facctconference.org/) | 🔵 [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 38 | 🟢 [FAccT](https://facctconference.org/) | 🔵 [J. Cybersecurity](https://academic.oup.com/cybersecurity) | 🔵 [ACM JRC](https://dl.acm.org/journal/jrc) |
| 39 | 🟢 [FAccT](https://facctconference.org/) | 🔵 [S&P Magazine](https://www.computer.org/csdl/magazine/sp) | 🔵 [CACM Practice](https://cacm.acm.org/) |
| 40 | 🔵 [Scientific Data](https://www.nature.com/sdata/) | 🔵 [Data in Brief](https://www.sciencedirect.com/journal/data-in-brief) / [NeurIPS D&B](https://neurips.cc/) / [DMLR](https://data.mlr.press) | — |
| 41 | 🔵 [CACM](https://cacm.acm.org/) | 🔵 [S&P Magazine](https://www.computer.org/csdl/magazine/sp) / [IEEE Computer](https://www.computer.org/) / [Queue](https://queue.acm.org/) | — |
| 42 | 🔵 [IEEE TSE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | 🔵 [ESE](https://link.springer.com/journal/10664) / [TOSEM](https://dl.acm.org/journal/tosem) / [ICSE](https://www.icse-conferences.org/) | — |
| 43 | 🟢 [WWW](https://www2027.thewebconf.org/) | 🔵 [AIES](https://www.aies-conference.com/) | 🔵 [FAccT](https://facctconference.org/) |
| 44 | 🟠 [EuroS&P](https://eurosp2027.ieee-security.org/)<br>🟠 [reg 25 Nov · papers 2 Dec](https://eurosp2027.ieee-security.org/cfp.html) | 🔵 [NDSS (next cycle)](https://www.ndss-symposium.org/) | 🔵 [CCS](https://www.sigsac.org/ccs/CCS2027/) / [USENIX Sec](https://www.usenix.org/conference/usenixsecurity27) |
| 45 | 🟢 [FAccT](https://facctconference.org/) | 🟡 [USENIX Sec C2](https://www.usenix.org/conference/usenixsecurity27)<br>🟡 [papers 26 Jan (reg 19 Jan)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 46 | 🟠 [AsiaCCS R2](https://asiaccs2027.cityu.edu.mo/)<br>🟠 [papers 11 Dec](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | 🟡 [SAIS](https://www.usenix.org/conference/sais27)<br>🟡 [papers 4 Feb](https://www.usenix.org/conference/sais27/call-for-papers) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 47 | 🟡 [SAIS](https://www.usenix.org/conference/sais27)<br>🟡 [papers 4 Feb](https://www.usenix.org/conference/sais27/call-for-papers) | 🔵 [EAAI](https://www.sciencedirect.com/journal/engineering-applications-of-artificial-intelligence) | 🔵 [Info Sciences](https://www.sciencedirect.com/journal/information-sciences) |
| 48 | 🟡 [ACM TOPS](https://dl.acm.org/journal/tops) | 🔵 [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | — |

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