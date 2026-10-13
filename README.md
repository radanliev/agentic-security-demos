<p align="center">
  <img src="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/assets/logo.svg" alt="Agentic Security Demos Logo" width="200">
</p>

<h1 align="center">Agentic AI Security Demos</h1>
<p align="center">
  <strong>A curated collection of 45 reproducible teaching demonstrations for agentic AI security, distilled from research targeting top-tier venues (SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, ICML, ICLR, AAAI, IJCAI, ACL, ICSE, WWW, EuroS&P, PoPETs, DSN, CSF, ACNS, Black Hat, DEF CON, TIFS, TDSC, TOPS, CSUR, COMST, TPAMI, TMLR, Nature MI, Computers & Security, Journal of Cybersecurity, IEEE S&P Magazine, Scientific Data, CACM, TSE, FAccT). All scenarios, numbers and verdicts here are synthetic coursework — they describe no real publication.</strong>
</p>

> 🐣 **Padawan-practice notice (read before citing).** These are my teaching demos by Petar Radanliev — training missions for the classroom, not Jedi trials. Like Padawan exercises, each demo **may or may not be converted into a full paper**, and any paper **may or may not be accepted** at its listed venue. The venue column names the *training ground* that inspired the exercise, never a publication claim. No preprints, no datasets deposited, no reviewer verdicts — just lightsabers set to stun (synthetic fixtures, offline only).

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
| 01 | **Blind Verification** | Cryptographic verification of agent outputs without trusted execution environments | ✅ Active |
| 02 | **Supply Chain AIBOM Drift** | AI Bill of Materials tracking & drift detection across model updates | ✅ Active |
| 03 | **Eval Design Invariants** | Statistically rigorous evaluation frameworks with invariant guarantees | ✅ Active |
| 04 | **Prompt Injection & Tool Authority** | Capability-based authority mediation for tool-using agents | ✅ Active |
| 05 | **Evidence Release Assurance** | Cryptographic evidence chains for agent accountability | ✅ Active |
| 06 | **Network Recon** | eBPF-backed network reconnaissance with formal admission control | ✅ Active |
| 07 | **Malware Triage** | Statistical reconstruction of malware triage decisions | ✅ Active |
| 08 | **File Inclusion** | Provenance-tracked file inclusion for agent workflows | ✅ Active |
| 09 | **MITM Interception** | Ephemeral buffer interception for credential extraction detection | ✅ Active |
| 10 | **Vulnerability Assessment** | Cross-vendor vulnerability scanning with authoritative taxonomy | ✅ Active |
| 11 | **Degenerate Reporting** | Meta-science audit: evaluations that cannot rule out do-nothing policies | ✅ Active |
| 12 | **Provenance-Bound Authorization** | Provenance-aware authorization for untrusted calendar content | ✅ Active |
| 13 | **Typed Commitments & Coverage Cues** | Wrong coverage cues and agreement-gate failures in LLM assessors | ✅ Active |
| 14 | **Conformal Action Gating** | Distribution-free risk control for tool execution and how it fails under benchmark shift | ✅ Active |
| 15 | **Hijack Probes** | Hidden-state signatures of instruction hijack in open-weight agents | ✅ Active |
| 16 | **Infection Spread** | Epidemic dynamics of prompt-injection propagation in multi-agent systems | ✅ Active |
| 17 | **Report Fidelity** | Claims-versus-logs fidelity of coding agents | ✅ Active |
| 18 | **Cross-lingual Gap** | Cross-lingual transfer of injections and the detector language gap | ✅ Active |
| 19 | **Lineage Risk** | Inherited risk along fine-tune lineages on the model hub | ✅ Active |
| 20 | **Agent Web Census** | Agent-facing files and in-the-wild injections across the web | ✅ Active 🔴 next deadline |
| 21 | **MCP Ecosystem Census** | Tool-poisoning exposure, rug-pull dynamics and capability surface across 36k MCP servers (toy census) | ✅ Active |
| 22 | **Memory Leakage** | Contextual-integrity leakage via agent memory stores | ✅ Active |
| 23 | **Fault Injection** | Dependability of agent pipelines under pipeline faults | ✅ Active |
| 24 | **Delegation Checks** | Authorization and agent-to-agent delegation properties | ✅ Active |
| 25 | **Attestation Verifier** | Install-time provenance verification for agent supply chains | ✅ Active |
| 26 | **Sandbox Probes** | Agent sandbox isolation and exfiltration controls | ✅ Active |
| 27 | **CI Trigger Scan** | Injection surface of coding agents wired to CI | ✅ Active |
| 28 | **Memory Poisoning** | Persistent memory poisoning and the MemScope auditor toy | ✅ Active |
| 29 | **Provenance Graphs** | Tamper-evident provenance for post-incident reconstruction | ✅ Active |
| 30 | **Default Configs** | Insecure defaults in self-hosted LLM stacks | ✅ Active |
| 31 | **Scope Creep** | OAuth scope over-privilege in agent integrations | ✅ Active |
| 32 | **Reproducibility Audit** | Artefact audit of the agent-security literature | ✅ Active |
| 33 | **Protocol Coverage** | Agent protocol element × threat coverage map | ✅ Active |
| 34 | **Visual Injection** | Typographic injection against vision-language agents | ✅ Active |
| 35 | **Scaling Meta-regression** | Agent misbehaviour versus scale across benchmarks | ✅ Active |
| 36 | **Card Debt** | Documentation debt across open model cards | ✅ Active |
| 37 | **Detector Cost** | Injection-detector comparison with false-positive cost | ✅ Active |
| 38 | **Assurance Claims** | System-card assurance claims versus obligations | ✅ Active |
| 39 | **Incident Taxonomy** | Agentic-AI threat taxonomy for practitioners | ✅ Active |
| 40 | **Corpus Union** | License-audited unified agentic-security corpus | ✅ Active |
| 41 | **Ten Invariants** | Security invariants checklist synthesis | ✅ Active |
| 42 | **Patch Lifecycle** | Vulnerability lifecycle and patch adoption lag | ✅ Active |
| 43 | **Terms Coding** | Platform terms accountability allocation | ✅ Active |
| 44 | **Toolflow Taint** | Cross-tool dataflow integrity tracking | ✅ Active |
| 45 | **Exact Nulls for Localisation Claims** | Exact hypergeometric significance for localisation claims, ratio-to-null transfer failures, second corpus, and design-limit corollary (`radanliev/demo-45-localisation-nulls`, private; available on request) | ✅ Active |
| 46 | | | 🚧 Skeleton |

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

# Run one demo's suite (folders demo-01 … demo-45)
make test DEMO=01
```

---

## 🚀 Quick Start

All demos run offline from the repository root — no API keys, no network.
Each demo folder also has step-by-step `INSTRUCTIONS.md` with expected outputs.

```bash
# Run a teaching demo (folders demo-01 … demo-45)
make demo DEMO=01   # Blind Verification
make demo DEMO=04   # Prompt Injection Authority
make demo DEMO=07   # Malware Triage
make demo DEMO=13   # Typed Commitments & Coverage Cues
make demo DEMO=14   # Conformal Action Gating (ICML toy)
make demo DEMO=21   # MCP Ecosystem Census (EuroS&P toy)
make demo DEMO=28   # Memory Poisoning (DEF CON toy)
make demo DEMO=44   # Toolflow Taint (CCS toy)
make demo DEMO=45   # Exact Nulls for Localisation Claims (SaTML toy)

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

> 🌌 **A long time ago in a classroom far, far away…** Every row below is a Padawan training
> ground, not a battle record. The *Plan A Venue* column names the nearest conference that matches
> the demo's title — each is an **Episode IV – A New Hope** mission at idea / planning stage
> that may or may not grow into a full paper, which may or may not be accepted. No preprints,
> no datasets deposited, no reviewer verdicts. The *Plan B Venue* and *Plan C Venue* columns are the escape routes
> if Plan A is rejected — your options map, in order. Venue names link to the conference (coloured by community: 🟦 security, 🟪 AI/ML, 🟩 software/web/society); deadline cells link to the
> submission pages (circled by urgency: 🔴 urgent, 🟠 soon, 🟡 upcoming). No Death Star plans have been transmitted yet.
>
> 🔴 = due October 2026 (urgent) · 🟠 = due November–December 2026 (soon) · 🟡 = due January 2027 (upcoming) · ♾️ *Rolling — no deadline* venues take submissions any time · ⏰ = date has passed · 🟦 = security community · 🟪 = AI/ML community · 🟩 = software, web & society community · ⚠️ same work cannot be under review in two places at once — backups run sequentially, never simultaneously.
>
> 🔀 **Plan A / Plan B: the WWW'27 first wave (7 research-track papers — the author cap).** Seven demos go to **[WWW'27, Dublin](https://www2027.thewebconf.org/)** first — abstract 18 Oct 2026, full paper 25 Oct 2026 ([submission via OpenReview](https://www2027.thewebconf.org/research-track-papers)). If rejected (notification 4 Jan 2027), each drops to its Plan B, then Plan C — always sequential, never simultaneous. Demo 28 goes as a WWW'27 **demo paper** (16 Nov 2026), which sits outside the 7-paper research-track cap. The cap is verified on the [call](https://www2027.thewebconf.org/research-track-papers/): papers beyond an author's first seven of one type, by submission ID, are desk-rejected.
>
> | Demo | Plan A (WWW'27 track) | Plan B | Plan C |
> |------|----------------------|--------|--------|
> | Demo 18 | Security and Privacy | ACL'27 (ARR Jan) | EMNLP'27 |
> | Demo 19 | Security and Privacy | ICSE'28 | FSE'28 |
> | Demo 20 | Web Infrastr. and Agentic Systems | WWW short 16 Nov'26 | IMC'27 |
> | Demo 21 | Security and Privacy | IMC'27 | AsiaCCS'28 |
> | Demo 27 | Web Infrastr. and Agentic Systems | Black Hat USA'27 | DEF CON Demo Labs |
> | Demo 36 | Responsible Web | Nature MI (post-rejection fallback only) | Patterns |
> | Demo 43 | Responsible Web | AIES'27 (post-rejection only) | FAccT'28 |
> | Demo 28 | S&P'27 C2 research paper (moved from WWW demo track) | DEF CON 35 | BH Arsenal |
>
> Date logic: EuroS&P'27 (25 Nov), BH Asia (20 Oct) and FAccT'27 (3 Nov) all fall inside the WWW review window (25 Oct–4 Jan), so they cannot back up a WWW rejection — Plan Bs above are all actionable after 4 Jan 2027.
>
> 🛡️ **Plan A / Plan B: the USENIX'27 Cycle 2 slate (3 papers).** Three demos go to **[USENIX Security '27, Denver](https://www.usenix.org/conference/usenixsecurity27)** — registration 19 Jan 2027, papers 26 Jan 2027, artifacts 29 Jan 2027 ([CFP](https://www.usenix.org/conference/usenixsecurity27/call-for-papers)). AsiaCCS R2 papers are locked in review — the three below are clear.
>
> | Demo | Plan B | Plan C |
> |------|--------|--------|
> | Demo 10 | ACSAC'27 | RAID'28 |
> | Demo 12 | NDSS'28 | CCS'28 |
> | Demo 13 | CSF'27 | EuroS&P'28 |
>
> Contingencies (not counted): demo-21 if WWW-rejected 4 Jan (22 days to rework). All papers need a mandatory Open Science appendix and anonymous artifact links (4open.science, ID `SEC27`).
>
> ⚖️ **Plan A / Plan B: the FAccT'27 slate (4 papers, no author cap).** Four demos go to **[FAccT'27, Porto](https://facctconference.org/)** — abstract 27 Oct 2026, paper 3 Nov 2026 ([CFP](https://facctconference.org/2027/cfp.html); accept/revise/reject 22 Dec 2026, revision due 28 Jan 2027). No per-author cap, but every author on every paper must sign up to review or face desk rejection. If rejected (final notification 23 Mar 2027), each drops to Plan B, then Plan C. None overlap the WWW or USENIX slates.
>
> | Demo | Plan B | Plan C |
> |------|--------|--------|
> | Demo 31 | TOPS | TDSC |
> | Demo 37 | CoSe | TDSC |
> | Demo 38 | JoC | CoSe |
> | Demo 39 | S&P Magazine | CACM Practice |
>
> Confirmed fourth: demo-37 is now Plan A FAccT'27 — CoSe held as Plan B, TDSC as Plan C. Demo-22 is held out — FAccT would force skipping PoPETs Issue 3. Demo 45 also lists FAccT'27 as its Plan A, so the FAccT'27 load is five papers, and the 2027 author guide asks every author of every paper to sign up as a reviewer.
>
> 🔐 **Plan A / Plan B: seven papers on the IEEE S&P'27 Cycle 2 slate.** Seven demos go to **IEEE S&P'27 Cycle 2** — abstract 10 Nov, papers 17 Nov 2026. A rejection drops each one to Plan B, then Plan C — always sequential, never simultaneous. None overlap the WWW, USENIX or FAccT slates.
>
> ⚠️ **Cap check (verified 13 Oct 2026 on the [S&P'27 call](https://sp2027.ieee-security.org/cfpapers.html)):** S&P'27 allows at most **6 papers per author per cycle**, enforced at abstract registration (10 Nov 2026). Above the cap, **all** of that author's registrations in the cycle are desk-rejected. This slate lists 7, so one must move before 10 Nov. Papers rejected at S&P must also wait one year before resubmitting there.
>
> | Demo | Plan B | Plan C |
> |------|--------|--------|
> | Demo 04 | USENIX Sec'28 / CCS'27 | CCS'27 |
> | Demo 09 | ESORICS'27 (spring cycle) | RAID'27 / ACSAC'27 |
> | Demo 26 | ACSAC'27 | DIMVA'28 |
> | Demo 28 | DEF CON 35 | BH Arsenal |
> | Demo 29 | TIFS | TDSC |
> | Demo 30 | TDSC | TIFS |
> | Demo 33 | COMST | Proc. IEEE |
>
> Demos 22, 23, 08, 25, 24 and 14 stay on their own venues (PoPETs, DSN, AsiaCCS, ACNS, CSF and ICML).
>
> 🔁 **Plan A / Plan B / Plan C: Demo 01, re-planned 13 Oct 2026.** One venue at a time, never simultaneously. Rule applied: Q1 journals only, and no author fees.
>
> | Plan | Venue | Deadline | First decision | Est. chance |
> |------|-------|----------|----------------|-------------|
> | A | 🟦 [Computers & Security](https://www.sciencedirect.com/journal/computers-and-security) (Elsevier; SJR 2025 Q1) | ♾️ rolling — submitting Oct 2026 | desk ~3 days; after review ~53 days | ~20% |
> | B | 🟦 [USENIX SAIS'27](https://www.usenix.org/conference/sais27/call-for-papers) (first edition; double-blind) | 🟠 4 Feb 2027 | 16 Mar 2027 | ~20% |
> | C | 🟦 [Journal of Information Security and Applications](https://www.sciencedirect.com/journal/journal-of-information-security-and-applications) (Elsevier; SJR 2025 Q1) | ♾️ rolling | ~2–4 months | ~25% |
>
> Fees: Plans A and C are hybrid Elsevier journals, so the subscription route costs the author nothing. [Oxford's publisher-deals page](https://www.bodleian.ox.ac.uk/open-research/open-access-publishing/journal-article/publisher-deals) lists Elsevier open access for an Oxford corresponding author who submits from an @ox.ac.uk address and picks CC BY; some UK institutions declined the 2026 Jisc–Elsevier agreement, so confirm Oxford's coverage at submission before choosing open access. The Open University deals exclude single-authored papers. Computers & Security uses single-anonymized review, a 10,000-word main-text limit and a 250-word abstract.
>
> Considered and not used: TMLR (diamond open access, no fees, but SCImago 2025 Q2 in AI); WWW'27 (research-track cap of 7 already used); S&P'27 C2 (cap of 6 already exceeded); FAccT'27 and PoPETs'27 (scope). Chances are estimates, not measured rates.

| Demo | Plan A Venue | Year | Deadline (AoE) | Plan B Venue | Plan C Venue |
|------|--------------|------|----------|---------------------------|--------------|
| 01 | 🟦 [Computers & Security](https://www.sciencedirect.com/journal/computers-and-security) | — | [♾️ Rolling — submitting Oct 2026 (Plan A)](https://www.sciencedirect.com/journal/computers-and-security/publish/guide-for-authors) | USENIX SAIS'27 (4 Feb 2027) | JISA |
| 02 | 🟩 [EMSE](https://link.springer.com/journal/10664) | — | [♾️ EMSE rolling](https://www.editorialmanager.com/emse) | IEEE TSE (only after an EMSE decision) | MSR'27 (only after a TSE decision) |
| 03 | 🟪 [NeurIPS](https://neurips.cc/) | 2027 | [NeurIPS'27 D&B CFP unpublished, TBD](https://neurips.cc/) | ICLR'28 / TMLR | TMLR |
| 04 | 🟦 IEEE S&P'27 C2 | 2027 | S&P'27 Cycle 2 papers 17 Nov 2026 (Plan A) | USENIX Sec'28 / CCS'27 | CCS'27 |
| 05 | 🟦 IEEE TDSC | — | ♾️ *Submitted Oct 2026 (formerly USENIX Security '27 C1, desk-rejected for introduction formatting)* | — | — |
| 06 | 🟦 [NDSS](https://www.ndss-symposium.org/) | 2028 | NDSS'28 (Plan A; USENIX Security removed as target) | TDSC | — |
| 07 | 🟦 [RAID](https://dl.acm.org/conference/raid) | 2027 | [RAID'27 CFP unpublished, TBD](https://dl.acm.org/conference/raid) | DIMVA'27 / ACSAC'27 | ESORICS'28 |
| 08 | 🟦 [ASIACCS](https://asiaccs2027.cityu.edu.mo/) | 2027 | 🟠 **[AsiaCCS'27 Round 2 papers 11 Dec 2026](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html)** | ESORICS'27 C2 / RAID'27 | RAID'28 |
| 09 | 🟦 IEEE S&P'27 C2 | 2027 | S&P'27 Cycle 2 papers 17 Nov 2026 (Plan A); [ESORICS'27 CFP unpublished, TBD](https://conf.laas.fr/esorics) (Plan B) | ESORICS'27 (spring cycle) | RAID'27 / ACSAC'27 |
| 10 | 🟦 [USENIX Security](https://www.usenix.org/conference/usenixsecurity27) | 2027 | 🟡 [USENIX'27 Cycle 2 papers 26 Jan 2027 (reg. 19 Jan)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | ACSAC'27 | RAID'28 |
| 11 | 🟦 [RAID](https://dl.acm.org/conference/raid) | 2027 | [RAID'27 CFP unpublished, TBD](https://dl.acm.org/conference/raid) | DIMVA'27 / ESORICS'28 | ESORICS'28 |
| 12 | 🟦 [USENIX Security](https://www.usenix.org/conference/usenixsecurity27) | 2027 | 🟡 [USENIX'27 Cycle 2 papers 26 Jan 2027](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | NDSS'28 / CCS'27 | CCS'28 |
| 13 | 🟦 [USENIX Security](https://www.usenix.org/conference/usenixsecurity27) | 2027 | 🟡 [USENIX'27 Cycle 2 papers 26 Jan 2027](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | CSF'27 / EuroS&P'27 | EuroS&P'28 |
| 14 | 🟪 [ICML](https://icml.cc/) | 2027 | 🟡 [ICML'27 abstract ~23 Jan 2027, paper ~28 Jan 2027 (projection)](https://icml.cc/) | TMLR / NeurIPS'27 / ICLR'28 | ICLR'28 |
| 15 | 🟪 [ICLR](https://iclr.cc/) | 2028 | [ICLR'28 abstract ~18 Sep 2027, paper ~25 Sep 2027 (projection)](https://iclr.cc/) | ICML'28 / TMLR / NeurIPS'27 | TMLR |
| 16 | 🟪 [AAAI](https://aaai.org/Conferences/AAAI) | 2028 | [AAAI'28 abstract ~late Jul 2027, paper ~early Aug 2027 (projection)](https://aaai.org/Conferences/AAAI) | IJCAI'28 / AAMAS'28 / SaTML'28 | AAMAS'28 |
| 17 | 🟪 [IJCAI](https://www.ijcai.org/) | 2027 | 🟡 [IJCAI'27 abstract 4 Jan 2027, paper 11 Jan 2027](https://2027.ijcai.org/) | AAAI'28 / AAMAS'28 / ECAI'27 | AAMAS'28 |
| 18 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🔴 <mark>**[WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)](https://www2027.thewebconf.org/research-track-papers)**</mark>; ARR Jan 2027 (Plan B) | ACL'27 (ARR Jan) | EMNLP'27 |
| 19 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🔴 <mark>**[WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)](https://www2027.thewebconf.org/research-track-papers)**</mark>; ICSE'28 abs ~23 Jun 2027 (Plan B) | ICSE'28 | FSE'28 |
| 20 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🔴 <mark>**[NEXT UP — WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026](https://www2027.thewebconf.org/research-track-papers)**</mark> | Short paper 16 Nov 2026 / IMC'27 / WWW'28 | IMC'27 |
| 21 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🔴 <mark>**[WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)](https://www2027.thewebconf.org/research-track-papers)**</mark> | IMC'27 | AsiaCCS'28 |
| 22 | 🟦 [PoPETs](https://petsymposium.org/2027) | 2027 | 🟠 **[PoPETs'27 Issue 3: 30 Nov 2026](https://petsymposium.org/cfp27.php)**; Issue 4: 28 Feb 2027 | PoPETs Iss. 4 / USENIX'28 C1 / CCS'27 | USENIX Sec'28 |
| 23 | 🟦 [DSN](https://dsn2027-berlin.github.io/) | 2027 | 🟠 **[DSN'27 abstract 25 Nov 2026; paper 2 Dec 2026](https://dsn2027-berlin.github.io/call-for-contributions)** | DSN'28 / ISSRE'27 / TDSC | TDSC |
| 24 | 🟦 [CSF](https://csf2027.ieee-security.org/) | 2027 | 🟡 [CSF'27 Winter cycle 28 Jan 2027](https://csf2027.ieee-security.org/cfp.html) | CSF'28 / ESORICS'27 C2 / CCS'27 | ESORICS'28 |
| 25 | 🟦 [ACNS](https://acns2027.isg.rhul.ac.uk/) | 2027 | 🟡 [ACNS'27 Cycle 2: 21 Jan 2027](https://acns2027.isg.rhul.ac.uk/calls/papers) | ESORICS'27 C2 / EuroS&P'28 / AsiaCCS'28 | EuroS&P'28 |
| 26 | 🟦 IEEE S&P'27 C2 | 2027 | S&P'27 Cycle 2 papers 17 Nov 2026 (Plan A); [ACSAC'27 ~26 May 2027 (projection)](https://submit.acsac.org/) (Plan B) | ACSAC'27 | DIMVA'28 / AsiaCCS'28 |
| 27 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🔴 <mark>**[WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)](https://www2027.thewebconf.org/research-track-papers)**</mark> | BH USA'27 / Arsenal (post-rejection only) | DEF CON Demo Labs |
| 28 | 🟦 IEEE S&P'27 C2 | 2027 | S&P'27 Cycle 2 research paper 17 Nov 2026 (Plan A); [DEF CON 35 CFP ~1 May 2027 (Plan B)](https://www.defcon.org/index.html) | DEF CON 35 / AI Village posters | BH Arsenal |
| 29 | 🟦 IEEE S&P'27 C2 | 2027 | S&P'27 Cycle 2 papers 17 Nov 2026 (Plan A); [TIFS ♾️ rolling](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) (Plan B) | TIFS | TDSC |
| 30 | 🟦 IEEE S&P'27 C2 | 2027 | S&P'27 Cycle 2 papers 17 Nov 2026 (Plan A); [TDSC ♾️ rolling](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) (Plan B) | TDSC | TIFS |
| 31 | 🟩 [FAccT](https://facctconference.org/) | 2027 | 🔴 <mark>**[FAccT'27 abstract 27 Oct 2026, paper 3 Nov 2026](https://facctconference.org/2027/cfp.html)**</mark> | TOPS | TDSC |
| 32 | 🟩 [ACM CSUR](https://dl.acm.org/journal/csur) | — | [♾️ *Rolling — no deadline*](https://dl.acm.org/journal/csur) | COMST / DTRAP / CSR | COMST |
| 33 | 🟦 IEEE S&P'27 C2 SoK | 2027 | S&P'27 Cycle 2 SoK papers 17 Nov 2026 (Plan A); [COMST ♾️ rolling](https://www.comsoc.org/publications/journals/ieee-comst/call-for-papers) (Plan B) | COMST | Proc. IEEE |
| 34 | 🟪 [IEEE TPAMI](https://www.computer.org/csdl/journal/tp) | — | [♾️ *Rolling — no deadline*](https://www.computer.org/csdl/journal/tp) | TNNLS / TIP / TIFS | TIFS |
| 35 | 🟪 [TMLR](https://jmlr.org/tmlr/) | — | [♾️ *Rolling — no deadline*](https://jmlr.org/tmlr/) | JMLR / DMLR / ICML'28 | JMLR |
| 36 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🔴 <mark>**[WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)](https://www2027.thewebconf.org/research-track-papers)**</mark>; Nature MI ♾️ rolling (Plan B) | Nature MI | Patterns |
| 37 | 🟩 [FAccT](https://facctconference.org/) | 2027 | 🔴 <mark>**[FAccT'27 abstract 27 Oct 2026, paper 3 Nov 2026](https://facctconference.org/2027/cfp.html)**</mark> | CoSe | TDSC |
| 38 | 🟩 [FAccT](https://facctconference.org/) | 2027 | 🔴 <mark>**[FAccT'27 abstract 27 Oct 2026, paper 3 Nov 2026](https://facctconference.org/2027/cfp.html)**</mark> | JoC | CoSe |
| 39 | 🟩 [FAccT](https://facctconference.org/) | 2027 | 🔴 <mark>**[FAccT'27 abstract 27 Oct 2026, paper 3 Nov 2026](https://facctconference.org/2027/cfp.html)**</mark> | S&P Magazine | CACM Practice |
| 40 | 🟩 [Scientific Data](https://www.nature.com/sdata/) | — | [♾️ *Rolling — no deadline*](https://www.nature.com/sdata/) | Data in Brief / NeurIPS'27 D&B / DMLR | NeurIPS'28 D&B |
| 41 | 🟩 [CACM](https://cacm.acm.org/) | — | [♾️ *Rolling (held until 3 accepts)*](https://cacm.acm.org/) | S&P Mag / Computer / Queue | ACM Queue |
| 42 | 🟩 [IEEE TSE](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | — | [♾️ *Rolling — no deadline*](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32) | ESE / TOSEM / ICSE journal-first | TOSEM |
| 43 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🔴 <mark>**[WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)](https://www2027.thewebconf.org/research-track-papers)**</mark> | AIES'27 | FAccT'28 |
| 44 | 🟦 [CCS](https://www.sigsac.org/ccs/CCS2027/) | 2027 | CCS'27 | NDSS'28 | — |
| 45 | 🟩 [FAccT](https://facctconference.org/) | 2027 | 🔴 <mark>**[FAccT'27 abstract 27 Oct 2026, paper 3 Nov 2026](https://facctconference.org/2027/cfp.html)**</mark> | USENIX Sec'27 C2 ([papers 26 Jan 2027, reg. 19 Jan](https://www.usenix.org/conference/usenixsecurity27/call-for-papers)) | [TDSC ♾️ rolling](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) |
| 46 | 🟦 [JISA](https://www.sciencedirect.com/journal/journal-of-information-security-and-applications) | — | ♾️ *Rolling — submit only after real-model rebuild (currently one-page skeleton, simulated models)* | [Computers & Security ♾️ rolling](https://www.sciencedirect.com/journal/computers-and-security) | [USENIX SAIS'27](https://www.usenix.org/conference/sais27/call-for-papers) (4 Feb 2027; check per-author cap first — several USENIX submissions) |

---

## 📖 Citation

If you use this collection in your research, please cite:

```bibtex
@misc{radanliev2026agenticsecuritydemos,
  title={Agentic AI Security Demos: A Reproducible Teaching Collection},
  author={Radanliev, Petar},
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

- **Oxford Lagrange** — fuel for the X-wings (compute credits)
- **GitHub Accelerator** — the hidden Rebel base (open-source support)
- **Anonymous reviewers** at SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, ICML, ICLR, AAAI, IJCAI, ACL, ICSE, WWW, EuroS&P, PoPETs, DSN, CSF, ACNS, TIFS, TDSC, TOPS, CSUR, COMST, TPAMI, TMLR, Nature MI, Computers & Security, Journal of Cybersecurity, Scientific Data, CACM, TSE, FAccT — the Jedi Council: wise, anonymous, occasionally striking back (Episode V)
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