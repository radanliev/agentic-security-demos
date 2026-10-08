<p align="center">
  <img src="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/assets/logo.svg" alt="Agentic Security Demos Logo" width="200">
</p>

<h1 align="center">Agentic AI Security Demos</h1>
<p align="center">
  <strong>A curated collection of 44 reproducible teaching demonstrations for agentic AI security, distilled from research targeting top-tier venues (SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, ICML, ICLR, AAAI, IJCAI, ACL, ICSE, WWW, EuroS&P, PoPETs, DSN, CSF, ACNS, Black Hat, DEF CON, TIFS, TDSC, TOPS, CSUR, COMST, TPAMI, TMLR, Nature MI, Computers & Security, Journal of Cybersecurity, IEEE S&P Magazine, Scientific Data, CACM, TSE, FAccT). All scenarios, numbers and verdicts here are synthetic coursework — they describe no real publication.</strong>
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

| # | Demo | Venue | Focus | Status |
|---|------|-------|-------|--------|
| 01 | **Blind Verification** | 🟦 SATML 2027 | Cryptographic verification of agent outputs without trusted execution environments | ✅ Active |
| 02 | **Supply Chain AIBOM Drift** | 🟩 TOSEM | AI Bill of Materials tracking & drift detection across model updates | ✅ Active |
| 03 | **Eval Design Invariants** | 🟪 NeurIPS 2027 | Statistically rigorous evaluation frameworks with invariant guarantees | ✅ Active |
| 04 | **Prompt Injection & Tool Authority** | 🟦 IEEE SP 2027 | Capability-based authority mediation for tool-using agents | ✅ Active |
| 05 | **Evidence Release Assurance** | 🟦 IEEE SP 2027 | Cryptographic evidence chains for agent accountability | ✅ Active |
| 06 | **Network Recon** | 🟦 [USENIX'27](https://www.usenix.org/conference/usenixsecurity27) (Plan A) / NDSS'28 (Plan B) | eBPF-backed network reconnaissance with formal admission control | ✅ Active |
| 07 | **Malware Triage** | 🟦 RAID 2027 | Statistical reconstruction of malware triage decisions | ✅ Active |
| 08 | **File Inclusion** | 🟦 ASIACCS 2027 | Provenance-tracked file inclusion for agent workflows | ✅ Active |
| 09 | **MITM Interception** | 🟦 [S&P'27](http://sp2027.ieee-security.org/) (Plan A) / ESORICS'27 (Plan B) | Ephemeral buffer interception for credential extraction detection | ✅ Active |
| 10 | **Vulnerability Assessment** | 🟦 [USENIX'27](https://www.usenix.org/conference/usenixsecurity27) (Plan A) / ACSAC'27 (Plan B) | Cross-vendor vulnerability scanning with authoritative taxonomy | ✅ Active |
| 11 | **Degenerate Reporting** | 🟦 [USENIX'27](https://www.usenix.org/conference/usenixsecurity27) SoK (Plan A) / RAID'27 (Plan B) | Meta-science audit: evaluations that cannot rule out do-nothing policies | ✅ Active |
| 12 | **Provenance-Bound Authorization** | 🟦 USENIX Security 2027 | Provenance-aware authorization for untrusted calendar content | ✅ Active |
| 13 | **Format vs Cueing** | 🟦 USENIX Security 2027 | Separating format constraint from coverage cueing in typed pre-reveal commitments | ✅ Active |
| 14 | **Conformal Action Gating** | 🟪 ICML 2027 | Distribution-free risk control for tool execution and how it fails under benchmark shift | ✅ Active |
| 15 | **Hijack Probes** | 🟪 ICLR 2028 | Hidden-state signatures of instruction hijack in open-weight agents | ✅ Active |
| 16 | **Infection Spread** | 🟪 AAAI 2028 | Epidemic dynamics of prompt-injection propagation in multi-agent systems | ✅ Active |
| 17 | **Report Fidelity** | 🟪 IJCAI 2027 | Claims-versus-logs fidelity of coding agents | ✅ Active |
| 18 | **Cross-lingual Gap** | 🟩 [WWW'27](https://www2027.thewebconf.org/) (Plan A) / ACL'27 (Plan B) | Cross-lingual transfer of injections and the detector language gap | ✅ Active |
| 19 | **Lineage Risk** | 🟩 [WWW'27](https://www2027.thewebconf.org/) (Plan A) / ICSE'28 (Plan B) | Inherited risk along fine-tune lineages on the model hub | ✅ Active |
| 20 | **Agent Web Census** | 🟩 WWW 2027 | Agent-facing files and in-the-wild injections across the web | ✅ Active 🔴 next deadline |
| 21 | **MCP Ecosystem Census** | 🟩 [WWW'27](https://www2027.thewebconf.org/) (Plan A) / EuroS&P'27 (Plan B) | Tool-poisoning exposure, rug-pull dynamics and capability surface across 36k MCP servers (toy census) | ✅ Active |
| 22 | **Memory Leakage** | 🟦 PoPETs 2027 | Contextual-integrity leakage via agent memory stores | ✅ Active |
| 23 | **Fault Injection** | 🟦 DSN 2027 | Dependability of agent pipelines under pipeline faults | ✅ Active |
| 24 | **Delegation Checks** | 🟦 CSF 2027 | Authorization and agent-to-agent delegation properties | ✅ Active |
| 25 | **Attestation Verifier** | 🟦 ACNS 2027 | Install-time provenance verification for agent supply chains | ✅ Active |
| 26 | **Sandbox Probes** | 🟦 [S&P'27](http://sp2027.ieee-security.org/) (Plan A) / ACSAC'27 (Plan B) | Agent sandbox isolation and exfiltration controls | ✅ Active |
| 27 | **CI Trigger Scan** | 🟩 [WWW'27](https://www2027.thewebconf.org/) (Plan A) / Black Hat'27 (Plan B) | Injection surface of coding agents wired to CI | ✅ Active |
| 28 | **Memory Poisoning** | 🟩 [WWW'27](https://www2027.thewebconf.org/) demo track (Plan A) / DEF CON 35 (Plan B) | Persistent memory poisoning and the MemScope auditor toy | ✅ Active |
| 29 | **Provenance Graphs** | 🟦 [S&P'27](http://sp2027.ieee-security.org/) (Plan A) / TIFS (Plan B) | Tamper-evident provenance for post-incident reconstruction | ✅ Active |
| 30 | **Default Configs** | 🟦 [S&P'27](http://sp2027.ieee-security.org/) (Plan A) / TDSC (Plan B) | Insecure defaults in self-hosted LLM stacks | ✅ Active |
| 31 | **Scope Creep** | 🟩 [FAccT'27](https://facctconference.org/) (Plan A) / TOPS (Plan B) | OAuth scope over-privilege in agent integrations | ✅ Active |
| 32 | **Reproducibility Audit** | 🟩 ACM CSUR | Artefact audit of the agent-security literature | ✅ Active |
| 33 | **Protocol Coverage** | 🟦 [S&P'27](http://sp2027.ieee-security.org/) SoK (Plan A) / COMST (Plan B) | Agent protocol element × threat coverage map | ✅ Active |
| 34 | **Visual Injection** | 🟪 IEEE TPAMI | Typographic injection against vision-language agents | ✅ Active |
| 35 | **Scaling Meta-regression** | 🟪 TMLR | Agent misbehaviour versus scale across benchmarks | ✅ Active |
| 36 | **Card Debt** | 🟩 [WWW'27](https://www2027.thewebconf.org/) (Plan A) / Nature MI (Plan B) | Documentation debt across open model cards | ✅ Active |
| 37 | **Detector Cost** | 🟦 Computers & Security | Injection-detector comparison with false-positive cost | ✅ Active |
| 38 | **Assurance Claims** | 🟩 [FAccT'27](https://facctconference.org/) (Plan A) / JoC (Plan B) | System-card assurance claims versus obligations | ✅ Active |
| 39 | **Incident Taxonomy** | 🟩 [FAccT'27](https://facctconference.org/) (Plan A) / S&P Mag (Plan B) | Agentic-AI threat taxonomy for practitioners | ✅ Active |
| 40 | **Corpus Union** | 🟩 Scientific Data | License-audited unified agentic-security corpus | ✅ Active |
| 41 | **Ten Invariants** | 🟩 CACM | Security invariants checklist synthesis | ✅ Active |
| 42 | **Patch Lifecycle** | 🟩 IEEE TSE | Vulnerability lifecycle and patch adoption lag | ✅ Active |
| 43 | **Terms Coding** | 🟩 [WWW'27](https://www2027.thewebconf.org/) (Plan A) / AIES'27 (Plan B) | Platform terms accountability allocation | ✅ Active |
| 44 | **Toolflow Taint** | 🟦 [USENIX'27](https://www.usenix.org/conference/usenixsecurity27) (Plan A) / CCS'27 (Plan B) | Cross-tool dataflow integrity tracking | ✅ Active |

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

# Run one demo's suite (folders demo-01 … demo-13)
make test DEMO=01
```

---

## 🚀 Quick Start

All demos run offline from the repository root — no API keys, no network.
Each demo folder also has step-by-step `INSTRUCTIONS.md` with expected outputs.

```bash
# Run a teaching demo (folders demo-01 … demo-44)
make demo DEMO=01   # Blind Verification
make demo DEMO=04   # Prompt Injection Authority
make demo DEMO=07   # Malware Triage
make demo DEMO=13   # Typed Commitments & Coverage Cues
make demo DEMO=14   # Conformal Action Gating (ICML toy)
make demo DEMO=21   # MCP Ecosystem Census (EuroS&P toy)
make demo DEMO=28   # Memory Poisoning (DEF CON toy)
make demo DEMO=44   # Toolflow Taint (CCS toy)

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
> 🔀 **Plan A / Plan B: the WWW'27 first wave (7 research-track papers — the author cap).** Seven demos go to **[WWW'27, Dublin](https://www2027.thewebconf.org/)** first — abstract 18 Oct 2026, full paper 25 Oct 2026 ([submission via OpenReview](https://www2027.thewebconf.org/research-track-papers)). If rejected (notification 4 Jan 2027), each drops to its Plan B, then Plan C — always sequential, never simultaneous. Demo 28 goes as a WWW'27 **demo paper** (16 Nov 2026), which sits outside the 7-paper research-track cap.
>
> | Demo | Plan A (WWW'27 track) | Plan B | Plan C |
> |------|----------------------|--------|--------|
> | 18 Cross-lingual Gap | Web Mining, Multilingual Content | ACL'27 (ARR Jan) | EMNLP'27 |
> | 19 Lineage Risk | Web Mining / Evaluation & Resources | ICSE'28 | FSE'28 |
> | 20 Agent Web Census | Web Infrastr. and Agentic Systems | WWW short 16 Nov'26 | IMC'27 |
> | 21 MCP Census | Security and Privacy | IMC'27 | AsiaCCS'28 |
> | 27 CI Trigger Scan | Web Infrastr. and Agentic Systems | Black Hat USA'27 | DEF CON Demo Labs |
> | 36 Card Debt | Web Mining / Evaluation & Resources | Nature MI | Patterns |
> | 43 Platform Terms | Web Econ. and Digital Society | AIES'27 | FAccT'28 |
> | 28 Memory Poisoning | Demo track (16 Nov 2026, outside cap) | DEF CON 35 | BH Arsenal |
>
> Date logic: EuroS&P'27 (25 Nov), BH Asia (20 Oct) and FAccT'27 (3 Nov) all fall inside the WWW review window (25 Oct–4 Jan), so they cannot back up a WWW rejection — Plan Bs above are all actionable after 4 Jan 2027.
>
> 🛡️ **Plan A / Plan B: the USENIX'27 Cycle 2 slate (6 papers).** Demo 5 goes to IEEE S&P'27 Cycle 2 Plan A, so six other demos go to **[USENIX Security '27, Denver](https://www.usenix.org/conference/usenixsecurity27)** — registration 19 Jan 2027, papers 26 Jan 2027, artifacts 29 Jan 2027 ([CFP](https://www.usenix.org/conference/usenixsecurity27/call-for-papers)). S&P C2 / AsiaCCS R2 papers are locked in review — the six below are clear.
>
> | Demo | USENIX angle | Plan B | Plan C |
> |------|-------------|--------|--------|
> | 06 Network Recon | eBPF admission control, systems core | NDSS'28 | TDSC |
> | 10 Vulnerability Assessment | cross-vendor measurement | ACSAC'27 | RAID'28 |
> | 11 Degenerate Reporting | reframe as **SoK** (`SoK:` title prefix) | RAID'27 | ESORICS'28 |
> | 12 Provenance Authz | already C2-bound | NDSS'28 | CCS'28 |
> | 13 Typed Commitments | already C2-bound | CSF'27 | EuroS&P'28 |
> | 44 Toolflow Taint | agent dispatch measurement | CCS'27 | NDSS'28 |
>
> Contingencies (not counted): demo-21 if WWW-rejected 4 Jan (22 days to rework); demo-4 only on S&P early-reject 18 Jan. All papers need a mandatory Open Science appendix and anonymous artifact links (4open.science, ID `SEC27`).
>
> ⚖️ **Plan A / Plan B: the FAccT'27 slate (4 papers, no author cap).** Four demos go to **[FAccT'27, Porto](https://facctconference.org/)** — abstract 27 Oct 2026, paper 3 Nov 2026 ([CFP](https://facctconference.org/2027/cfp.html); accept/revise/reject 22 Dec 2026, revision due 28 Jan 2027). No per-author cap, but every author on every paper must sign up to review or face desk rejection. If rejected (final notification 23 Mar 2027), each drops to Plan B, then Plan C. None overlap the WWW or USENIX slates; all originals are rolling venues held for after.
>
> | Demo | FAccT angle | Plan B | Plan C |
> |------|------------|--------|--------|
> | 31 Scope Creep | consent meaningfulness: requested vs used scopes + breakage of least-privilege policy | TOPS | TDSC |
> | 37 Detector Cost | detector comparison with false-positive cost | CoSe | TDSC |
> | 38 Assurance Claims | transparency documentation vs regulation | JoC | CoSe |
> | 39 Incident Taxonomy | incident-grounded harms, practitioner controls | S&P Magazine | CACM Practice |
>
> Confirmed fourth: demo-37 (detector evaluation) is now Plan A FAccT'27 — CoSe held as Plan B, TDSC as Plan C. Demo-22 is held out — FAccT would force skipping PoPETs Issue 3.
>
> 🔐 **Plan A / Plan B: the IEEE S&P'27 Cycle 2 slate (6 papers — the per-author cap).** Demo 4 plus five more go to **[IEEE S&P'27, Montreal](http://sp2027.ieee-security.org/)** — abstract registration 10 Nov 2026 (the 6-paper cap is enforced at registration), full paper 17 Nov 2026 ([CFP](http://sp2027.ieee-security.org/cfpapers.html); early reject 18 Jan 2027, final notification 5 Mar 2027). Every demo below has its original venue due after the S&P decision, so a rejection drops it to Plan B, then Plan C — always sequential, never simultaneous. A rejected paper cannot return to S&P for a year. None overlap the WWW, USENIX or FAccT slates.
>
> | Demo | S&P angle | Plan B | Plan C |
> |------|-----------|--------|--------|
> | 04 AuthorityBound | already C2-bound | USENIX Sec'28 / CCS'27 | CCS'27 |
> | 09 InterceptBound | provenance-bounded interception agent, live range | ESORICS'27 (spring cycle) | RAID'27 / ACSAC'27 |
> | 30 Default Configs | insecure-defaults census with vendor-vs-operator attribution | TDSC | TIFS |
> | 26 Sandbox Probes | isolation and exfiltration across agent sandboxes | ACSAC'27 | DIMVA'28 |
> | 29 Provenance Graphs | logging sufficiency for attributing agent actions after an incident | TIFS | TDSC |
> | 33 Protocol Coverage | SoK: security of agent communication protocols | COMST | Proc. IEEE |
>
> Date logic: PoPETs'27 Issue 3 (30 Nov), DSN'27 (2 Dec), AsiaCCS'27 R2 (11 Dec), ACNS'27 C2 (21 Jan), CSF'27 Winter (28 Jan) and ICML'27 (~28 Jan) all fall inside the S&P review window (17 Nov–~5 Mar), so demos 22, 23, 08, 25, 24 and 14 stay on their own venues. Alternates (swap in only before the 10 Nov registration, never as a seventh): demo-32 as an SoK (instead of 33), demo-42.

| Demo | Plan A Venue | Year | Deadline (AoE) | Plan B Venue | Plan C Venue |
|------|--------------|------|----------|---------------------------|--------------|
| 01 | 🟦 [SATML](https://satml.org/) | 2027 | [SaTML'27 papers 29 Sep 2026 ⏰](https://satml.org/call-for-papers) | USENIX Sec'28 / S&P'28 next cycles | S&P'28 |
| 02 | 🟩 [TOSEM](https://dl.acm.org/journal/tosem) | — | [♾️ TOSEM rolling](https://mc.manuscriptcentral.com/tosem) | CCS'27 (only after a TOSEM decision) | EMSE (only after a CCS decision) |
| 03 | 🟪 [NeurIPS](https://neurips.cc/) | 2027 | [NeurIPS'27 D&B CFP unpublished, TBD](https://neurips.cc/) | ICLR'28 / TMLR | TMLR |
| 04 | 🟦 [IEEE SP](http://sp2027.ieee-security.org/) | 2027 | 🟠 **[S&P'27 Cycle 2 papers 17 Nov 2026 (abstract 10 Nov) — due in weeks](http://sp2027.ieee-security.org/cfpapers.html)** | USENIX Sec'28 / CCS'27 | CCS'27 |
| 05 | 🟦 [IEEE SP](http://sp2027.ieee-security.org/) | 2027 | 🟠 **[S&P'27 Cycle 2: abstract 10 Nov, paper 17 Nov 2026 (Plan A)](http://sp2027.ieee-security.org/cfpapers.html)** | EuroS&P'27 / AsiaCCS'27 | NDSS'28 |
| 06 | 🟦 [USENIX Security](https://www.usenix.org/conference/usenixsecurity27) | 2027 | 🟡 [USENIX'27 Cycle 2 papers 26 Jan 2027 (reg. 19 Jan)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | NDSS'28 | TDSC |
| 07 | 🟦 [RAID](https://dl.acm.org/conference/raid) | 2027 | [RAID'27 CFP unpublished, TBD](https://dl.acm.org/conference/raid) | DIMVA'27 / ACSAC'27 | ESORICS'28 |
| 08 | 🟦 [ASIACCS](https://asiaccs2027.cityu.edu.mo/) | 2027 | 🟠 **[AsiaCCS'27 Round 2 papers 11 Dec 2026](https://asiaccs2027.cityu.edu.mo/call-for-papers/index.html)** | ESORICS'27 C2 / RAID'27 | RAID'28 |
| 09 | 🟦 [IEEE SP](http://sp2027.ieee-security.org/) | 2027 | 🟠 **[S&P'27 Cycle 2: abstract 10 Nov, paper 17 Nov 2026 (Plan A)](http://sp2027.ieee-security.org/cfpapers.html)**; [ESORICS'27 CFP unpublished, TBD](https://conf.laas.fr/esorics) (Plan B) | ESORICS'27 (spring cycle) | RAID'27 / ACSAC'27 |
| 10 | 🟦 [USENIX Security](https://www.usenix.org/conference/usenixsecurity27) | 2027 | 🟡 [USENIX'27 Cycle 2 papers 26 Jan 2027 (reg. 19 Jan)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | ACSAC'27 | RAID'28 |
| 11 | 🟦 [USENIX Security](https://www.usenix.org/conference/usenixsecurity27) (SoK) | 2027 | 🟡 [USENIX'27 Cycle 2 papers 26 Jan 2027 (reg. 19 Jan)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | RAID'27 | ESORICS'28 |
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
| 26 | 🟦 [IEEE SP](http://sp2027.ieee-security.org/) | 2027 | 🟠 **[S&P'27 Cycle 2: abstract 10 Nov, paper 17 Nov 2026 (Plan A)](http://sp2027.ieee-security.org/cfpapers.html)**; [ACSAC'27 ~26 May 2027 (projection)](https://submit.acsac.org/) (Plan B) | ACSAC'27 | DIMVA'28 / AsiaCCS'28 |
| 27 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🔴 <mark>**[WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)](https://www2027.thewebconf.org/research-track-papers)**</mark> | BH USA'27 / Arsenal | DEF CON Demo Labs |
| 28 | 🟩 [WWW'27](https://www2027.thewebconf.org/) | 2027 | 🟠 <mark>**[WWW'27 demo paper 16 Nov 2026 (Plan A)](https://www2027.thewebconf.org/demos/)**</mark>; [DEF CON 35 CFP ~1 May 2027 (Plan B)](https://www.defcon.org/index.html) | DEF CON 35 / AI Village posters | BH Arsenal |
| 29 | 🟦 [IEEE SP](http://sp2027.ieee-security.org/) | 2027 | 🟠 **[S&P'27 Cycle 2: abstract 10 Nov, paper 17 Nov 2026 (Plan A)](http://sp2027.ieee-security.org/cfpapers.html)**; [TIFS ♾️ rolling](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206) (Plan B) | TIFS | TDSC |
| 30 | 🟦 [IEEE SP](http://sp2027.ieee-security.org/) | 2027 | 🟠 **[S&P'27 Cycle 2: abstract 10 Nov, paper 17 Nov 2026 (Plan A)](http://sp2027.ieee-security.org/cfpapers.html)**; [TDSC ♾️ rolling](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=8858) (Plan B) | TDSC | TIFS |
| 31 | 🟩 [FAccT](https://facctconference.org/) | 2027 | 🔴 <mark>**[FAccT'27 abstract 27 Oct 2026, paper 3 Nov 2026](https://facctconference.org/2027/cfp.html)**</mark> | TOPS | TDSC |
| 32 | 🟩 [ACM CSUR](https://dl.acm.org/journal/csur) | — | [♾️ *Rolling — no deadline*](https://dl.acm.org/journal/csur) | COMST / DTRAP / CSR | COMST |
| 33 | 🟦 [IEEE SP](http://sp2027.ieee-security.org/) (SoK) | 2027 | 🟠 **[S&P'27 Cycle 2: abstract 10 Nov, paper 17 Nov 2026 (Plan A)](http://sp2027.ieee-security.org/cfpapers.html)**; [COMST ♾️ rolling](https://www.comsoc.org/publications/journals/ieee-comst/call-for-papers) (Plan B) | COMST | Proc. IEEE |
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
| 44 | 🟦 [USENIX Security](https://www.usenix.org/conference/usenixsecurity27) | 2027 | 🟡 [USENIX'27 Cycle 2 papers 26 Jan 2027 (reg. 19 Jan)](https://www.usenix.org/conference/usenixsecurity27/call-for-papers) | CCS'27 | NDSS'28 |

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