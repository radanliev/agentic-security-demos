<p align="center">
  <img src="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/assets/logo.svg" alt="Agentic Security Demos Logo" width="200">
</p>

<h1 align="center">Agentic AI Security Demos</h1>
<p align="center">
  <strong>A curated collection of 47 reproducible teaching demonstrations for agentic AI security, distilled from research targeting top-tier venues (SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, ICML, ICLR, AAAI, IJCAI, ACL, ICSE, WWW, EuroS&P, PoPETs, DSN, CSF, ACNS, Black Hat, DEF CON, TIFS, TDSC, TOPS, CSUR, COMST, TPAMI, TMLR, Nature MI, Journal of Cybersecurity, IEEE S&P Magazine, Scientific Data, CACM, TSE, FAccT). All scenarios, numbers and verdicts here are synthetic coursework — they describe no real publication.</strong>
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
| 01 | **Blind Verification** | Cryptographic verification of agent outputs without trusted execution environments | <font color="#1a7f37">**Submitted**</font> |
| 02 | **Supply Chain AIBOM Drift** | AI Bill of Materials tracking & drift detection across model updates | <font color="#1a7f37">**Submitted**</font> |
| 03 | **Eval Design Invariants** | Statistically rigorous evaluation frameworks with invariant guarantees | ✅ Active |
| 04 | **Prompt Injection & Tool Authority** | Capability-based authority mediation for tool-using agents | <font color="#953800">**S&P C2 17 Nov**</font> |
| 05 | **Evidence Release Assurance** | Cryptographic evidence chains for agent accountability | <font color="#1a7f37">**Submitted**</font> |
| 06 | **Network Recon** | eBPF-backed network reconnaissance with formal admission control | ✅ Active |
| 07 | **Malware Triage** | Statistical reconstruction of malware triage decisions | ✅ Active |
| 08 | **File Inclusion** | Provenance-tracked file inclusion for agent workflows | <font color="#953800">**AsiaCCS R2 11 Dec**</font> |
| 09 | **MITM Interception** | Ephemeral buffer interception for credential extraction detection | <font color="#953800">**S&P C2 17 Nov**</font> |
| 10 | **Vulnerability Assessment** | Cross-vendor vulnerability scanning with authoritative taxonomy | <font color="#9a6700">**USENIX C2 26 Jan**</font> |
| 11 | **Degenerate Reporting** | Meta-science audit: evaluations that cannot rule out do-nothing policies | ✅ Active |
| 12 | **Provenance-Bound Authorization** | Provenance-aware authorization for untrusted calendar content | <font color="#9a6700">**USENIX C2 26 Jan**</font> |
| 13 | **Typed Commitments & Coverage Cues** | Wrong coverage cues and agreement-gate failures in LLM assessors | <font color="#9a6700">**USENIX C2 26 Jan**</font> |
| 14 | **Conformal Action Gating** | Distribution-free risk control for tool execution and how it fails under benchmark shift | <font color="#9a6700">**ICML ~28 Jan**</font> |
| 15 | **Hijack Probes** | Hidden-state signatures of instruction hijack in open-weight agents | ✅ Active |
| 16 | **Infection Spread** | Epidemic dynamics of prompt-injection propagation in multi-agent systems | ✅ Active |
| 17 | **Report Fidelity** | Claims-versus-logs fidelity of coding agents | <font color="#9a6700">**IJCAI 4 Jan**</font> |
| 18 | **Cross-lingual Gap** | Cross-lingual transfer of injections and the detector language gap | <font color="#cf222e">**WWW paper 25 Oct**</font> |
| 19 | **Lineage Risk** | Inherited risk along fine-tune lineages on the model hub | <font color="#cf222e">**WWW paper 25 Oct**</font> |
| 20 | **Agent Web Census** | Agent-facing files and in-the-wild injections across the web | <font color="#cf222e">**WWW paper 25 Oct**</font> |
| 21 | **MCP Ecosystem Census** | Tool-poisoning exposure, rug-pull dynamics and capability surface across 36k MCP servers (toy census) | <font color="#cf222e">**WWW paper 25 Oct**</font> |
| 22 | **Memory Leakage** | Contextual-integrity leakage via agent memory stores | <font color="#953800">**PoPETs 30 Nov**</font> |
| 23 | **Fault Injection** | Dependability of agent pipelines under pipeline faults | <font color="#953800">**DSN abs 25 Nov**</font> |
| 24 | **Delegation Checks** | Authorization and agent-to-agent delegation properties | <font color="#9a6700">**CSF 28 Jan**</font> |
| 25 | **Attestation Verifier** | Install-time provenance verification for agent supply chains | <font color="#9a6700">**ACNS 21 Jan**</font> |
| 26 | **Sandbox Probes** | Agent sandbox isolation and exfiltration controls | <font color="#953800">**S&P C2 17 Nov**</font> |
| 27 | **CI Trigger Scan** | Injection surface of coding agents wired to CI | <font color="#cf222e">**WWW paper 25 Oct**</font> |
| 28 | **Memory Poisoning** | Persistent memory poisoning and the MemScope auditor toy | <font color="#953800">**WWW demo 16 Nov**</font> |
| 29 | **Provenance Graphs** | Tamper-evident provenance for post-incident reconstruction | <font color="#953800">**S&P C2 17 Nov**</font> |
| 30 | **Default Configs** | Insecure defaults in self-hosted LLM stacks | <font color="#953800">**S&P C2 17 Nov**</font> |
| 31 | **Scope Creep** | OAuth scope over-privilege in agent integrations | <font color="#cf222e">**FAccT abstr. 27 Oct**</font> |
| 32 | **Reproducibility Audit** | Artefact audit of the agent-security literature | ✅ Active |
| 33 | **Protocol Coverage** | Agent protocol element × threat coverage map | <font color="#953800">**S&P C2 17 Nov**</font> |
| 34 | **Visual Injection** | Typographic injection against vision-language agents | ✅ Active |
| 35 | **Scaling Meta-regression** | Agent misbehaviour versus scale across benchmarks | ✅ Active |
| 36 | **Card Debt** | Documentation debt across open model cards | <font color="#cf222e">**WWW paper 25 Oct**</font> |
| 37 | **Detector Cost** | Injection-detector comparison with false-positive cost | <font color="#cf222e">**FAccT abstr. 27 Oct**</font> |
| 38 | **Assurance Claims** | System-card assurance claims versus obligations | <font color="#cf222e">**FAccT abstr. 27 Oct**</font> |
| 39 | **Incident Taxonomy** | Agentic-AI threat taxonomy for practitioners | <font color="#cf222e">**FAccT abstr. 27 Oct**</font> |
| 40 | **Corpus Union** | License-audited unified agentic-security corpus | ✅ Active |
| 41 | **Ten Invariants** | Security invariants checklist synthesis | ✅ Active |
| 42 | **Patch Lifecycle** | Vulnerability lifecycle and patch adoption lag | ✅ Active |
| 43 | **Terms Coding** | Platform terms accountability allocation | <font color="#cf222e">**WWW paper 25 Oct**</font> |
| 44 | **Toolflow Taint** | Cross-tool dataflow integrity tracking | <font color="#9a6700">**CCS ~mid-Jan (TBD)**</font> |
| 45 | **Exact Nulls for Localisation Claims** | Exact hypergeometric significance for localisation claims, ratio-to-null transfer failures, second corpus, and design-limit corollary (`radanliev/demo-45-localisation-nulls`, private; available on request) | <font color="#cf222e">**FAccT abstr. 27 Oct**</font> |
| 46 | **Embedding-swap cosine shift** | `1 - cosine` on two synthetic vectors, compared with the frozen simulated-study mean 0.1222 (`radanliev/demo-46-simulated-embedding-drift-aibom`, private) | <font color="#953800">**AsiaCCS R2 11 Dec**</font> |
| 47 | **Pre-reveal Seal** | Hash a localisation commitment before the answer key opens; a post-seal edit is a mismatch (`demo-47-blind-verification-eval-sais`, private; available on request) | <font color="#9a6700">**SAIS 4 Feb**</font> |

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

# Run one demo's suite (folders demo-01 … demo-47)
make test DEMO=01
```

---

## 🚀 Quick Start

All demos run offline from the repository root — no API keys, no network.
Each demo folder also has step-by-step `INSTRUCTIONS.md` with expected outputs.

```bash
# Run a teaching demo (folders demo-01 … demo-47)
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

> Every row is one demo's venue plan: **Plan A** first, and the **Plan B** / **Plan C**
> backup activates only after Plan A's decision — the same work is never under review in
> two places at once. Venue names link to the conference page. Deadline cells link to the
> submission page and show the **abstract and full-paper deadlines** (or *Rolling* for
> continuous submissions, *TBD* while the CFP is unpublished, *(projection)* where the
> venue has not yet announced). Colour code: <font color="#1a7f37">**green = submitted**</font> ·
> <font color="#cf222e">**red = nearest deadlines**</font> ·
> <font color="#953800">**orange = due November–December 2026**</font> ·
> <font color="#9a6700">**yellow = due January–February 2027**</font> ·
> <font color="#0969da">**blue = rolling or date not yet announced**</font>.

- **WWW'27 first wave — 7 research-track papers, the per-author cap** (a paper of the same type beyond an author's first seven is desk-rejected): demos 18, 19, 20, 21, 27, 36, 43. Notifications 4 Jan 2027; fallbacks open after that. Demo 28 goes as a WWW'27 **demo paper**, outside the cap.
- **USENIX Security'27 Cycle 2 slate — 3 papers**: demos 10, 12, 13; artifacts due 29 Jan 2027. The AsiaCCS'27 Round 2 papers (demos 08, 46) are locked in review across this window.
- **FAccT'27 slate — 5 papers, no author cap**: demos 31, 37, 38, 39, 45. Every author on every FAccT paper must sign up to review or the paper risks desk rejection.
- **IEEE S&P'27 Cycle 2 slate — 6 papers, exactly the per-author cycle cap** (enforced at abstract registration; a rejected S&P paper waits one year before resubmitting there): demos 04, 09, 26, 29, 30, 33. Demo 28 moved to the WWW'27 demo track.

| Demo | Plan A venue | Plan A deadline | Plan B venue | Plan B deadline | Plan C venue | Plan C deadline |
|------|--------------|-----------------|--------------|-----------------|--------------|-----------------|
| 01 | [<font color="#1a7f37">Expert Systems with Applications</font>](https://www.sciencedirect.com/journal/expert-systems-with-applications) | <font color="#1a7f37">**Submitted**</font> | [ACM TOSEM](https://dl.acm.org/journal/tosem) | Rolling | [Information Processing & Management](https://www.sciencedirect.com/journal/information-processing-and-management) | Rolling |
| 02 | [<font color="#1a7f37">EMSE</font>](https://link.springer.com/journal/10664) | <font color="#1a7f37">**Submitted**</font> | [IEEE TSE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | Rolling | MSR'27 | TBD |
| 03 | [<font color="#0969da">NeurIPS'27 (D&B)</font>](https://neurips.cc/) | [<font color="#0969da">**TBD (CFP unpublished)**</font>](https://neurips.cc/) | [ICLR'28 / TMLR](https://iclr.cc/) | TBD | [TMLR](https://jmlr.org/tmlr/) | Rolling |
| 04 | [<font color="#953800">IEEE S&P'27 C2</font>](https://sp2027.ieee-security.org/cfpapers.html) | [<font color="#953800">**abstract 10 Nov, papers 17 Nov**</font>](https://sp2027.ieee-security.org/cfpapers.html) | USENIX Sec'28 | TBD | CCS'27 (Cycle B) | TBD |
| 05 | [<font color="#1a7f37">IEEE TDSC</font>](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | <font color="#1a7f37">**Submitted**</font> | — | — | — | — |
| 06 | [<font color="#0969da">NDSS'28</font>](https://www.ndss-symposium.org/) | <font color="#0969da">**TBD (CFP unpublished)**</font> | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling |
| 07 | [<font color="#0969da">RAID'27</font>](https://dl.acm.org/conference/raid) | [<font color="#0969da">**TBD (CFP unpublished)**</font>](https://dl.acm.org/conference/raid) | DIMVA'27 / ACSAC'27 | TBD | ESORICS'28 | TBD |
| 08 | [<font color="#953800">AsiaCCS'27 (Round 2)</font>](https://asiaccs2027.cityu.edu.mo/) | [<font color="#953800">**papers 11 Dec**</font>](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | ESORICS'27 C2 / RAID'27 | TBD | RAID'28 | TBD |
| 09 | [<font color="#953800">IEEE S&P'27 C2</font>](https://sp2027.ieee-security.org/cfpapers.html) | [<font color="#953800">**abstract 10 Nov, papers 17 Nov**</font>](https://sp2027.ieee-security.org/cfpapers.html) | [ESORICS'27 (spring cycle)](https://conf.laas.fr/esorics) | TBD | RAID'27 / ACSAC'27 | TBD |
| 10 | [<font color="#9a6700">USENIX Security'27 (Cycle 2)</font>](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | [<font color="#9a6700">**papers 26 Jan 2027 (registration 19 Jan)**</font>](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | ACSAC'27 | TBD | RAID'28 | TBD |
| 11 | [<font color="#0969da">RAID'27</font>](https://dl.acm.org/conference/raid) | [<font color="#0969da">**TBD (CFP unpublished)**</font>](https://dl.acm.org/conference/raid) | DIMVA'27 / ESORICS'28 | TBD | ESORICS'28 | TBD |
| 12 | [<font color="#9a6700">USENIX Security'27 (Cycle 2)</font>](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | [<font color="#9a6700">**papers 26 Jan 2027 (registration 19 Jan)**</font>](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | NDSS'28 / CCS'27 | TBD | CCS'28 | TBD |
| 13 | [<font color="#9a6700">USENIX Security'27 (Cycle 2)</font>](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | [<font color="#9a6700">**papers 26 Jan 2027 (registration 19 Jan)**</font>](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | CSF'27 / EuroS&P'27 | TBD | EuroS&P'28 | TBD |
| 14 | [<font color="#9a6700">ICML'27</font>](https://icml.cc/) | [<font color="#9a6700">**abstract ~23 Jan, papers ~28 Jan 2027 (projection)**</font>](https://icml.cc/) | TMLR / NeurIPS'27 / ICLR'28 | TBD | ICLR'28 | TBD |
| 15 | [<font color="#0969da">ICLR'28</font>](https://iclr.cc/) | [<font color="#0969da">**abstract ~18 Sep 2027, papers ~25 Sep 2027 (projection)**</font>](https://iclr.cc/) | ICML'28 / TMLR / NeurIPS'27 | TBD | [TMLR](https://jmlr.org/tmlr/) | Rolling |
| 16 | [<font color="#0969da">AAAI'28</font>](https://aaai.org/Conferences/AAAI) | [<font color="#0969da">**abstract ~late Jul 2027, papers ~early Aug 2027 (projection)**</font>](https://aaai.org/Conferences/AAAI) | IJCAI'28 / AAMAS'28 / SaTML'28 | TBD | AAMAS'28 | TBD |
| 17 | [<font color="#9a6700">IJCAI'27</font>](https://www.ijcai.org/) | [<font color="#9a6700">**abstract 4 Jan, papers 11 Jan 2027**</font>](https://2027.ijcai.org/) | AAAI'28 / AAMAS'28 / ECAI'27 | TBD | AAMAS'28 | TBD |
| 18 | [<font color="#cf222e">WWW'27</font>](https://www2027.thewebconf.org/) | [<font color="#cf222e">**abstract 18 Oct (submitted), papers 25 Oct**</font>](https://www2027.thewebconf.org/research-track-papers) | ACL'27 (ARR Jan) | TBD | EMNLP'27 | TBD |
| 19 | [<font color="#cf222e">WWW'27</font>](https://www2027.thewebconf.org/) | [<font color="#cf222e">**abstract 18 Oct (submitted), papers 25 Oct**</font>](https://www2027.thewebconf.org/research-track-papers) | ICSE'28 | abstract ~23 Jun 2027 | FSE'28 | TBD |
| 20 | [<font color="#cf222e">WWW'27</font>](https://www2027.thewebconf.org/) | [<font color="#cf222e">**abstract 18 Oct (submitted), papers 25 Oct**</font>](https://www2027.thewebconf.org/research-track-papers) | WWW short papers / IMC'27 / WWW'28 | 16 Nov 2026 | IMC'27 | TBD |
| 21 | [<font color="#cf222e">WWW'27</font>](https://www2027.thewebconf.org/) | [<font color="#cf222e">**abstract 18 Oct (submitted), papers 25 Oct**</font>](https://www2027.thewebconf.org/research-track-papers) | IMC'27 | TBD | AsiaCCS'28 | TBD |
| 22 | [<font color="#953800">PoPETs'27</font>](https://petsymposium.org/2027) | [<font color="#953800">**Issue 3: 30 Nov**</font>](https://petsymposium.org/cfp27.php) | [PoPETs'27 Issue 4](https://petsymposium.org/cfp27.php) | 28 Feb 2027 | USENIX Sec'28 | TBD |
| 23 | [<font color="#953800">DSN'27</font>](https://dsn2027-berlin.github.io/) | [<font color="#953800">**abstract 25 Nov, papers 2 Dec**</font>](https://dsn2027-berlin.github.io/call-for-contributions) | DSN'28 / ISSRE'27 | TBD | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling |
| 24 | [<font color="#9a6700">CSF'27 (Winter cycle)</font>](https://csf2027.ieee-security.org/) | [<font color="#9a6700">**papers 28 Jan 2027**</font>](https://csf2027.ieee-security.org/cfp.html) | CSF'28 / ESORICS'27 C2 / CCS'27 | TBD | ESORICS'28 | TBD |
| 25 | [<font color="#9a6700">ACNS'27 (Cycle 2)</font>](https://acns2027.isg.rhul.ac.uk/) | [<font color="#9a6700">**papers 21 Jan 2027**</font>](https://acns2027.isg.rhul.ac.uk/calls/papers) | ESORICS'27 C2 / EuroS&P'28 / AsiaCCS'28 | TBD | EuroS&P'28 | TBD |
| 26 | [<font color="#953800">IEEE S&P'27 C2</font>](https://sp2027.ieee-security.org/cfpapers.html) | [<font color="#953800">**abstract 10 Nov, papers 17 Nov**</font>](https://sp2027.ieee-security.org/cfpapers.html) | [ACSAC'27](https://submit.acsac.org/) | ~26 May 2027 (projection) | DIMVA'28 / AsiaCCS'28 | TBD |
| 27 | [<font color="#cf222e">WWW'27</font>](https://www2027.thewebconf.org/) | [<font color="#cf222e">**abstract 18 Oct (submitted), papers 25 Oct**</font>](https://www2027.thewebconf.org/research-track-papers) | Black Hat USA'27 / Arsenal (post-rejection) | TBD | DEF CON Demo Labs | TBD |
| 28 | [<font color="#953800">WWW'27 Demo track</font>](https://www2027.thewebconf.org/demos/) | [<font color="#953800">**papers 16 Nov**</font>](https://www2027.thewebconf.org/demos/) | [DEF CON 35](https://www.defcon.org/index.html) | ~1 May 2027 (projection) | Black Hat Arsenal | TBD |
| 29 | [<font color="#953800">IEEE S&P'27 C2</font>](https://sp2027.ieee-security.org/cfpapers.html) | [<font color="#953800">**abstract 10 Nov, papers 17 Nov**</font>](https://sp2027.ieee-security.org/cfpapers.html) | [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | Rolling | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling |
| 30 | [<font color="#953800">IEEE S&P'27 C2</font>](https://sp2027.ieee-security.org/cfpapers.html) | [<font color="#953800">**abstract 10 Nov, papers 17 Nov**</font>](https://sp2027.ieee-security.org/cfpapers.html) | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling | [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | Rolling |
| 31 | [<font color="#cf222e">FAccT'27</font>](https://facctconference.org/) | [<font color="#cf222e">**abstract 27 Oct, papers 3 Nov**</font>](https://facctconference.org/2027/cfp.html) | ACM TOPS | Rolling | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling |
| 32 | [<font color="#0969da">ACM CSUR</font>](https://dl.acm.org/journal/csur) | [<font color="#0969da">**Rolling**</font>](https://dl.acm.org/journal/csur) | IEEE COMST / DTRAP / CSR | TBD | IEEE COMST | Rolling |
| 33 | [<font color="#953800">IEEE S&P'27 C2 SoK</font>](https://sp2027.ieee-security.org/cfpapers.html) | [<font color="#953800">**abstract 10 Nov, SoK papers 17 Nov**</font>](https://sp2027.ieee-security.org/cfpapers.html) | [IEEE COMST](https://www.comsoc.org/publications/journals/ieee-comst/call-for-papers) | Rolling | Proc. IEEE | Rolling |
| 34 | [<font color="#0969da">IEEE TPAMI</font>](https://www.computer.org/csdl/journal/tp) | [<font color="#0969da">**Rolling**</font>](https://www.computer.org/csdl/journal/tp) | TNNLS / TIP / TIFS | TBD | [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | Rolling |
| 35 | [<font color="#0969da">TMLR</font>](https://jmlr.org/tmlr/) | [<font color="#0969da">**Rolling**</font>](https://jmlr.org/tmlr/) | JMLR / DMLR / ICML'28 | TBD | [JMLR](https://jmlr.org/tmlr/) | Rolling |
| 36 | [<font color="#cf222e">WWW'27</font>](https://www2027.thewebconf.org/) | [<font color="#cf222e">**abstract 18 Oct (submitted), papers 25 Oct**</font>](https://www2027.thewebconf.org/research-track-papers) | Nature Machine Intelligence (post-rejection only) | Rolling | Patterns | TBD |
| 37 | [<font color="#cf222e">FAccT'27</font>](https://facctconference.org/) | [<font color="#cf222e">**abstract 27 Oct, papers 3 Nov**</font>](https://facctconference.org/2027/cfp.html) | [IEEE TIFS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) | Rolling | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling |
| 38 | [<font color="#cf222e">FAccT'27</font>](https://facctconference.org/) | [<font color="#cf222e">**abstract 27 Oct, papers 3 Nov**</font>](https://facctconference.org/2027/cfp.html) | [Journal of Cybersecurity](https://academic.oup.com/cybersecurity) | Rolling | [ACM J. Responsible Computing](https://dl.acm.org/journal/jrc) | Rolling |
| 39 | [<font color="#cf222e">FAccT'27</font>](https://facctconference.org/) | [<font color="#cf222e">**abstract 27 Oct, papers 3 Nov**</font>](https://facctconference.org/2027/cfp.html) | IEEE S&P Magazine | TBD | CACM Practice | TBD |
| 40 | [<font color="#0969da">Scientific Data</font>](https://www.nature.com/sdata/) | [<font color="#0969da">**Rolling**</font>](https://www.nature.com/sdata/) | Data in Brief / NeurIPS'27 D&B / DMLR | TBD | NeurIPS'28 D&B | TBD |
| 41 | [<font color="#0969da">CACM</font>](https://cacm.acm.org/) | [<font color="#0969da">**Rolling (held until 3 accepts)**</font>](https://cacm.acm.org/) | IEEE S&P Magazine / IEEE Computer / ACM Queue | TBD | ACM Queue | Rolling |
| 42 | [<font color="#0969da">IEEE TSE</font>](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | [<font color="#0969da">**Rolling**</font>](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | ESE / TOSEM / ICSE journal-first | TBD | [ACM TOSEM](https://dl.acm.org/journal/tosem) | Rolling |
| 43 | [<font color="#cf222e">WWW'27</font>](https://www2027.thewebconf.org/) | [<font color="#cf222e">**abstract 18 Oct (submitted), papers 25 Oct**</font>](https://www2027.thewebconf.org/research-track-papers) | AIES'27 (post-rejection only) | TBD | FAccT'28 | TBD |
| 44 | [<font color="#9a6700">CCS'27</font>](https://www.sigsac.org/ccs/CCS2027/) | <font color="#9a6700">**CFP TBD — expected Cycle A ~mid-Jan 2027, Cycle B ~late Apr 2027**</font> | NDSS'28 | TBD | — | — |
| 45 | [<font color="#cf222e">FAccT'27</font>](https://facctconference.org/) | [<font color="#cf222e">**abstract 27 Oct, papers 3 Nov**</font>](https://facctconference.org/2027/cfp.html) | [USENIX Security'27 (Cycle 2)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | papers 26 Jan 2027 (registration 19 Jan) | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling |
| 46 | [<font color="#953800">AsiaCCS'27 (Round 2)</font>](https://asiaccs2027.cityu.edu.mo/) | [<font color="#953800">**papers 11 Dec**</font>](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html) | [USENIX SAIS'27](https://www.usenix.org/conference/sais27/call-for-papers) | 4 Feb 2027 | [IEEE TDSC](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) | Rolling |
| 47 | [<font color="#9a6700">USENIX SAIS'27</font>](https://www.usenix.org/conference/sais27/call-for-papers) | [<font color="#9a6700">**papers 4 Feb 2027**</font>](https://www.usenix.org/conference/sais27/call-for-papers) | [Engineering Applications of AI](https://www.sciencedirect.com/journal/engineering-applications-of-artificial-intelligence) | Rolling | [Information Sciences](https://www.sciencedirect.com/journal/information-sciences) | Rolling |

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