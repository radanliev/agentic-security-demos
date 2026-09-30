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
| 01 | **Blind Verification** | SATML 2027 | Cryptographic verification of agent outputs without trusted execution environments | ✅ Active |
| 02 | **Supply Chain AIBOM Drift** | TOSEM / CCS 2027 | AI Bill of Materials tracking & drift detection across model updates | ✅ Active |
| 03 | **Eval Design Invariants** | NeurIPS 2027 | Statistically rigorous evaluation frameworks with invariant guarantees | ✅ Active |
| 04 | **Prompt Injection & Tool Authority** | IEEE SP 2027 | Capability-based authority mediation for tool-using agents | ✅ Active |
| 05 | **Evidence Release Assurance** | USENIX Security 2027 | Cryptographic evidence chains for agent accountability | ✅ Active |
| 06 | **Network Recon** | NDSS 2028 | eBPF-backed network reconnaissance with formal admission control | ✅ Active |
| 07 | **Malware Triage** | RAID 2027 | Statistical reconstruction of malware triage decisions | ✅ Active |
| 08 | **File Inclusion** | ASIACCS 2027 | Provenance-tracked file inclusion for agent workflows | ✅ Active |
| 09 | **MITM Interception** | ESORICS 2027 | Ephemeral buffer interception for credential extraction detection | ✅ Active |
| 10 | **Vulnerability Assessment** | ACSAC 2027 | Cross-vendor vulnerability scanning with authoritative taxonomy | ✅ Active |
| 11 | **Degenerate Reporting** | RAID 2027 | Meta-science audit: evaluations that cannot rule out do-nothing policies | ✅ Active |
| 12 | **Provenance-Bound Authorization** | USENIX Security 2027 | Provenance-aware authorization for untrusted calendar content | ✅ Active |
| 13 | **Format vs Cueing** | USENIX Security 2027 | Separating format constraint from coverage cueing in typed pre-reveal commitments | ✅ Active |
| 14 | **Conformal Action Gating** | ICML 2027 | Distribution-free risk control for tool execution and how it fails under benchmark shift | ✅ Active |
| 15 | **Hijack Probes** | ICLR 2028 | Hidden-state signatures of instruction hijack in open-weight agents | ✅ Active |
| 16 | **Infection Spread** | AAAI 2028 | Epidemic dynamics of prompt-injection propagation in multi-agent systems | ✅ Active |
| 17 | **Report Fidelity** | IJCAI 2027 | Claims-versus-logs fidelity of coding agents | ✅ Active |
| 18 | **Cross-lingual Gap** | ACL 2027 | Cross-lingual transfer of injections and the detector language gap | ✅ Active |
| 19 | **Lineage Risk** | [WWW'27](https://www2027.thewebconf.org/) (Plan A) / ICSE'28 (Plan B) | Inherited risk along fine-tune lineages on the model hub | ✅ Active |
| 20 | **Agent Web Census** | WWW 2027 | Agent-facing files and in-the-wild injections across the web | ✅ Active 🔴 next deadline |
| 21 | **MCP Ecosystem Census** | [WWW'27](https://www2027.thewebconf.org/) (Plan A) / EuroS&P'27 (Plan B) | Tool-poisoning exposure, rug-pull dynamics and capability surface across 36k MCP servers (toy census) | ✅ Active |
| 22 | **Memory Leakage** | PoPETs 2027 | Contextual-integrity leakage via agent memory stores | ✅ Active |
| 23 | **Fault Injection** | DSN 2027 | Dependability of agent pipelines under pipeline faults | ✅ Active |
| 24 | **Delegation Checks** | CSF 2027 | Authorization and agent-to-agent delegation properties | ✅ Active |
| 25 | **Attestation Verifier** | ACNS 2027 | Install-time provenance verification for agent supply chains | ✅ Active |
| 26 | **Sandbox Probes** | ACSAC 2027 | Agent sandbox isolation and exfiltration controls | ✅ Active |
| 27 | **CI Trigger Scan** | [WWW'27](https://www2027.thewebconf.org/) (Plan A) / Black Hat'27 (Plan B) | Injection surface of coding agents wired to CI | ✅ Active |
| 28 | **Memory Poisoning** | [WWW'27](https://www2027.thewebconf.org/) demo track (Plan A) / DEF CON 35 (Plan B) | Persistent memory poisoning and the MemScope auditor toy | ✅ Active |
| 29 | **Provenance Graphs** | IEEE TIFS | Tamper-evident provenance for post-incident reconstruction | ✅ Active |
| 30 | **Default Configs** | IEEE TDSC | Insecure defaults in self-hosted LLM stacks | ✅ Active |
| 31 | **Scope Creep** | ACM TOPS | OAuth scope over-privilege in agent integrations | ✅ Active |
| 32 | **Reproducibility Audit** | ACM CSUR | Artefact audit of the agent-security literature | ✅ Active |
| 33 | **Protocol Coverage** | IEEE COMST | Agent protocol element × threat coverage map | ✅ Active |
| 34 | **Visual Injection** | IEEE TPAMI | Typographic injection against vision-language agents | ✅ Active |
| 35 | **Scaling Meta-regression** | TMLR | Agent misbehaviour versus scale across benchmarks | ✅ Active |
| 36 | **Card Debt** | [WWW'27](https://www2027.thewebconf.org/) (Plan A) / Nature MI (Plan B) | Documentation debt across open model cards | ✅ Active |
| 37 | **Detector Cost** | Computers & Security | Injection-detector comparison with false-positive cost | ✅ Active |
| 38 | **Assurance Claims** | Journal of Cybersecurity | System-card assurance claims versus obligations | ✅ Active |
| 39 | **Incident Taxonomy** | IEEE S&P Magazine | Agentic-AI threat taxonomy for practitioners | ✅ Active |
| 40 | **Corpus Union** | Scientific Data | License-audited unified agentic-security corpus | ✅ Active |
| 41 | **Ten Invariants** | CACM | Security invariants checklist synthesis | ✅ Active |
| 42 | **Patch Lifecycle** | IEEE TSE | Vulnerability lifecycle and patch adoption lag | ✅ Active |
| 43 | **Terms Coding** | FAccT 2027 | Platform terms accountability allocation | ✅ Active |
| 44 | **Toolflow Taint** | CCS 2027 | Cross-tool dataflow integrity tracking | ✅ Active |

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
> ground, not a battle record. The *Plan A* column names the nearest conference that matches
> the demo's title — each is an **Episode IV – A New Hope** mission at idea / planning stage
> that may or may not grow into a full paper, which may or may not be accepted. No preprints,
> no datasets deposited, no reviewer verdicts. The *Backup plan* column is the escape route
> if Plan A is rejected. No Death Star plans have been transmitted yet.
>
> 🔴 <mark>**highlight**</mark> = due October 2026 (urgent) · 🟠 **bold** = due November–December 2026 (soon) · ♾️ *Rolling — no deadline* venues take submissions any time · ⏰ = date has passed · 🔀 = Plan A / Plan B routing (WWW'27 first, original venue on rejection) · ⚠️ same work cannot be under review in two places at once — backups run sequentially, never simultaneously.
>
> 🔀 **Plan A / Plan B: the WWW'27 first wave.** Five demos go to **[WWW'27, Dublin](https://www2027.thewebconf.org/)** first — abstract 18 Oct 2026, full paper 25 Oct 2026 ([submission via OpenReview](https://www2027.thewebconf.org/research-track-papers); demo papers 16 Nov 2026). If rejected, each drops to its original venue (Plan B). Max 7 submissions per author; page 1 of every paper must state its Web relevance or it is desk-rejected.
>
> | Demo | Plan A (WWW'27 track) | Plan B (original venue) |
> |------|----------------------|-------------------------|
> | 19 Lineage Risk | Web Mining / Evaluation & Resources | ICSE'28 |
> | 21 MCP Census | Security and Privacy | EuroS&P'27 |
> | 27 CI Trigger Scan | Web Infrastructure and Agentic Systems (or short paper) | Black Hat'27 |
> | 28 Memory Poisoning | Demo track (16 Nov 2026) | DEF CON 35 |
> | 36 Card Debt | Web Mining / Evaluation & Resources | Nature MI |

| Demo | Venue (training ground) | Year | Plan A | Deadline (AoE) | Backup plan (if rejected) |
|------|--------------------|------|--------|----------|---------------------------|
| 01 | SATML | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | SaTML'27 papers 29 Sep 2026 ⏰ | USENIX Sec'28 / S&P'28 next cycles |
| 02 | TOSEM / CCS | — / 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | TOSEM ♾️ rolling (primary); CCS'27 two cycles TBD (backup) | CCS'27 paper (backup); then EMSE |
| 03 | NeurIPS | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | NeurIPS'27 D&B CFP unpublished, TBD | ICLR'28 / TMLR |
| 04 | IEEE SP | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | 🟠 **S&P'27 Cycle 2 papers 17 Nov 2026 — due in weeks** | USENIX Sec'28 / CCS'27 |
| 05 | USENIX Security | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | USENIX'27 Cycle 1 submitted 25 Aug 2026, training continues | NDSS'28 / S&P'28 (if C1 rejected) |
| 06 | NDSS | 2028 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | NDSS'27 cycles passed; NDSS'28 CFP unpublished, TBD | USENIX Sec'28 / RAID'27 |
| 07 | RAID | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | RAID'27 CFP unpublished, TBD | DIMVA'27 / ACSAC'27 |
| 08 | ASIACCS | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | 🟠 **AsiaCCS'27 Round 2 papers 11 Dec 2026** | ESORICS'27 C2 / RAID'27 |
| 09 | ESORICS | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ESORICS'27 CFP unpublished, TBD | RAID'27 / ACSAC'27 |
| 10 | ACSAC | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ACSAC'27 CFP unpublished, TBD | SaTML'28 / RAID'27 |
| 11 | RAID | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | RAID'27 CFP unpublished, TBD | ACSAC'27 / ESORICS'27 |
| 12 | USENIX Security | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | USENIX'27 Cycle 2 papers 26 Jan 2027 | NDSS'28 / CCS'27 |
| 13 | USENIX Security | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | USENIX'27 Cycle 2 papers 26 Jan 2027 | CSF'27 / EuroS&P'27 |
| 14 | ICML | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ICML'27 abstract ~23 Jan 2027, paper ~28 Jan 2027 (projection from ICML 2026) | TMLR / NeurIPS'27 / ICLR'28 |
| 15 | ICLR | 2028 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ICLR'28 abstract ~18 Sep 2027, paper ~25 Sep 2027 (projection from ICLR 2027) | ICML'28 / TMLR / NeurIPS'27 |
| 16 | AAAI | 2028 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | AAAI'28 abstract ~late Jul 2027, paper ~early Aug 2027 (projection from AAAI-27) | IJCAI'28 / AAMAS'28 / SaTML'28 |
| 17 | IJCAI | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | IJCAI'27 abstract ~12 Jan 2027, paper ~19 Jan 2027 (projection from IJCAI 2026) | AAAI'28 / AAMAS'28 / ECAI'27 |
| 18 | ACL | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ACL'27 ARR Jan 2027 cycle (exact date TBA) | EMNLP'27 (ARR May) / NAACL'28 |
| 19 | WWW'27 🔀 (Plan A) / ICSE'28 (Plan B) | 2027 | 📨 [Submit to WWW'27 (OpenReview)](https://www2027.thewebconf.org/research-track-papers) | <mark>**WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)**</mark>; ICSE'28 abs ~23 Jun 2027 (Plan B) | Plan B: ICSE'28; then FSE'28 / TSE journal-first |
| 20 | WWW | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | 🔴 <mark>**NEXT UP — WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026**</mark> | Short paper 16 Nov 2026 / IMC'27 / WWW'28 |
| 21 | WWW'27 🔀 (Plan A) / EuroS&P'27 (Plan B) | 2027 | 📨 [Submit to WWW'27 (OpenReview)](https://www2027.thewebconf.org/research-track-papers) | <mark>**WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)**</mark>; EuroS&P abs 25 Nov 2026 (Plan B) | Plan B: EuroS&P'27; then AsiaCCS'27 R2 / IMC'27 / ESORICS'27 |
| 22 | PoPETs | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | 🟠 **PoPETs'27 Issue 3: 30 Nov 2026**; Issue 4: 28 Feb 2027 | PoPETs Iss. 4 / USENIX'28 C1 / CCS'27 |
| 23 | DSN | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | 🟠 **DSN'27 abstract 25 Nov 2026; paper 2 Dec 2026** | DSN'28 / ISSRE'27 / TDSC |
| 24 | CSF | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | CSF'27 Winter cycle 28 Jan 2027 | CSF'28 / ESORICS'27 C2 / CCS'27 |
| 25 | ACNS | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ACNS'27 Cycle 2: 21 Jan 2027 | ESORICS'27 C2 / EuroS&P'28 / AsiaCCS'28 |
| 26 | ACSAC | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ACSAC'27 ~26 May 2027 (projection from ACSAC 2026) | RAID'27 / DIMVA'27 / AsiaCCS'28 |
| 27 | WWW'27 🔀 (Plan A) / Black Hat'27 (Plan B) | 2027 | 📨 [Submit to WWW'27 (OpenReview)](https://www2027.thewebconf.org/research-track-papers) | <mark>**WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)**</mark>; BH Asia 20 Oct 2026 (Plan B) | Plan B: BH USA'27 / Arsenal |
| 28 | WWW'27 demo 🔀 (Plan A) / DEF CON 35 (Plan B) | 2027 | 📨 [Submit WWW'27 demo paper (OpenReview)](https://www2027.thewebconf.org/research-track-papers) | <mark>**WWW'27 demo paper 16 Nov 2026 (Plan A)**</mark>; DEF CON 35 CFP ~1 May 2027 (Plan B) | Plan B: DEF CON 35 / AI Village posters |
| 29 | IEEE TIFS | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | TDSC / TOPS / CoSe |
| 30 | IEEE TDSC | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | TIFS / TOPS / IEEE TRel |
| 31 | ACM TOPS | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | TDSC / CoSe / DTRAP |
| 32 | ACM CSUR | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | COMST / DTRAP / CSR |
| 33 | IEEE COMST | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | CSUR / Proc. IEEE / IEEE Network |
| 34 | IEEE TPAMI | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | TNNLS / TIP / TIFS |
| 35 | TMLR | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | JMLR / DMLR / ICML'28 |
| 36 | WWW'27 🔀 (Plan A) / Nature MI (Plan B) | 2027 | 📨 [Submit to WWW'27 (OpenReview)](https://www2027.thewebconf.org/research-track-papers) | <mark>**WWW'27 abstract 18 Oct 2026, paper 25 Oct 2026 (Plan A)**</mark>; Nature MI ♾️ rolling (Plan B) | Plan B: Nature MI; then Patterns / Nature Comms / SciData |
| 37 | Computers & Security | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | JISA / TDSC / DTRAP |
| 38 | Journal of Cybersecurity | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | CoSe / DTRAP / Policy & Internet |
| 39 | IEEE S&P Magazine | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | CACM Practice / ;login: / IEEE Computer |
| 40 | Scientific Data | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | Data in Brief / NeurIPS'27 D&B / DMLR |
| 41 | CACM | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling (CACM synthesis held until 3 programme papers accepted)* | S&P Mag / Computer / Queue |
| 42 | IEEE TSE | — | 🌟 Episode IV mission (idea stage — may or may not become a paper) | ♾️ *Rolling — no deadline* | ESE / TOSEM / ICSE journal-first |
| 43 | FAccT | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | 🔴 <mark>**FAccT'27 abstract 27 Oct 2026, paper 3 Nov 2026 — due in weeks**</mark> | AIES'27 / FAccT'28 / JoC Perspectives |
| 44 | CCS | 2027 | 🌟 Episode IV mission (idea stage — may or may not become a paper) | CCS'27 two cycles, dates TBD | USENIX Sec'28 / NDSS'28 |

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