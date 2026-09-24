<p align="center">
  <img src="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/assets/logo.svg" alt="Agentic Security Demos Logo" width="200">
</p>

<h1 align="center">Agentic AI Security Demos</h1>
<p align="center">
  <strong>A curated collection of 13 reproducible teaching demonstrations for agentic AI security, distilled from research targeting top-tier venues (SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC). All scenarios, numbers and verdicts here are synthetic coursework — they describe no real publication.</strong>
</p>

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
| 02 | **Supply Chain AIBOM Drift** | CCS 2027 | AI Bill of Materials tracking & drift detection across model updates | ✅ Active |
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
# Run a teaching demo (folders demo-01 … demo-13)
make demo DEMO=01   # Blind Verification
make demo DEMO=04   # Prompt Injection Authority
make demo DEMO=07   # Malware Triage
make demo DEMO=13   # Typed Commitments & Coverage Cues

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
| **Evidence Immutability** | SHA-256 sealed reference outputs in each demo's `results/` (Zenodo deposit on acceptance) |
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

| Demo | Venue (paper target) | Year | Paper | Artifact | Deadline (AoE, verified 2026-09-20) |
|------|--------------------|------|-------|----------|-------------------------------------|
| 01 | SATML | 2027 | Under review, no preprint | On acceptance | SaTML'27 papers 29 Sep 2026 |
| 02 | CCS | 2027 | Under review, no preprint | On acceptance | CCS'27 two cycles, dates TBD |
| 03 | NeurIPS | 2027 | Under review, no preprint | On acceptance | NeurIPS'27 D&B CFP unpublished, TBD |
| 04 | IEEE SP | 2027 | Under review, no preprint | On acceptance | S&P'27 Cycle 2 papers 17 Nov 2026 |
| 05 | USENIX Security | 2027 | Under review, no preprint | On acceptance | USENIX'27 Cycle 1 submitted 25 Aug 2026, under review |
| 06 | NDSS | 2028 | Under review, no preprint | On acceptance | NDSS'27 cycles passed; NDSS'28 CFP unpublished, TBD |
| 07 | RAID | 2027 | Under review, no preprint | On acceptance | RAID'27 CFP unpublished, TBD |
| 08 | ASIACCS | 2027 | Under review, no preprint | On acceptance | AsiaCCS'27 Round 2 papers 11 Dec 2026 |
| 09 | ESORICS | 2027 | Under review, no preprint | On acceptance | ESORICS'27 CFP unpublished, TBD |
| 10 | ACSAC | 2027 | Under review, no preprint | On acceptance | ACSAC'27 CFP unpublished, TBD |
| 11 | RAID | 2027 | Under review, no preprint | On acceptance | RAID'27 CFP unpublished, TBD |
| 12 | USENIX Security | 2027 | Under review, no preprint | On acceptance | USENIX'27 Cycle 2 papers 26 Jan 2027 |
| 13 | USENIX Security | 2027 | Preregistration draft, no data, no preprint | On acceptance | USENIX'27 Cycle 2 papers 26 Jan 2027 |

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

We welcome contributions that advance agentic AI security research! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- 🐛 Reporting vulnerabilities or reproducibility issues
- 💡 Proposing new demos or venues
- 🔀 Submitting pull requests (evidence-backed changes only)
- 🧪 Extending test suites
- 📝 Improving documentation

**Research Contribution Guidelines:**
1. All claims must be backed by frozen evidence packages
2. Statistical claims require pre-registered analysis plans
3. New demos must target a top-tier venue with clear scope
4. Breaking changes require RFC process

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

Individual demos may have additional licenses for third-party components (see `DEPENDENCIES.md`).

---

## 🙏 Acknowledgments

- **Oxford Lagrange** for compute credits
- **GitHub Accelerator** for open-source support
- **Anonymous reviewers** at SaTML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC
- **Agentic AI Security community** for feedback and replication

---

<p align="center">
  <strong>Advancing the science of agentic AI security, one reproducible demo at a time.</strong>
</p>

<p align="center">
  <a href="https://github.com/radanliev/agentic-security-demos/stargazers">⭐ Star</a> •
  <a href="https://github.com/radanliev/agentic-security-demos/fork">🍴 Fork</a> •
  <a href="https://github.com/radanliev/agentic-security-demos/issues">🐛 Report Issue</a> •
  <a href="https://github.com/radanliev/agentic-security-demos/discussions">💬 Discuss</a>
</p>