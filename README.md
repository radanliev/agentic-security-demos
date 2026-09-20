<p align="center">
  <img src="https://raw.githubusercontent.com/radanliev/agentic-security-demos/main/assets/logo.svg" alt="Agentic Security Demos Logo" width="200">
</p>

<h1 align="center">Agentic AI Security Demos</h1>
<p align="center">
  <strong>A curated collection of 12 reproducible demonstrations for agentic AI security research, spanning top-tier venues (SATML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, SACMAT).</strong>
</p>

<p align="center">
  <a href="https://github.com/radanliev/agentic-security-demos/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/radanliev/agentic-security-demos/ci.yml?branch=main&label=Build&style=flat-square" alt="Build Status"></a>
  <a href="https://pypi.org/project/agentic-security-demos/"><img src="https://img.shields.io/pypi/v/agentic-security-demos?style=flat-square&label=PyPI" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/agentic-security-demos/"><img src="https://img.shields.io/pypi/pyversions/agentic-security-demos?style=flat-square" alt="Python Versions"></a>
  <a href="https://github.com/radanliev/agentic-security-demos/blob/main/LICENSE"><img src="https://img.shields.io/github/license/radanliev/agentic-security-demos?style=flat-square" alt="License"></a>
  <a href="https://github.com/radanliev/agentic-security-demos/stargazers"><img src="https://img.shields.io/github/stars/radanliev/agentic-security-demos?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/radanliev/agentic-security-demos/issues"><img src="https://img.shields.io/github/issues/radanliev/agentic-security-demos?style=flat-square" alt="Issues"></a>
  <a href="https://zenodo.org/records/?q=agentic-security-demos"><img src="https://img.shields.io/badge/Zenodo-DOI-007EC6?style=flat-square" alt="Zenodo DOI"></a>
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
| 01 | **Blind Verification** | SATML 2026 | Cryptographic verification of agent outputs without trusted execution environments | ✅ Active |
| 02 | **Supply Chain AIBOM Drift** | CCS 2026 | AI Bill of Materials tracking & drift detection across model updates | ✅ Active |
| 03 | **Eval Design Invariants** | NeurIPS 2026 | Statistically rigorous evaluation frameworks with invariant guarantees | ✅ Active |
| 04 | **Prompt Injection & Tool Authority** | IEEE SP 2026 | Capability-based authority mediation for tool-using agents | ✅ Active |
| 05 | **Evidence Release Assurance** | USENIX Security 2026 | Cryptographic evidence chains for agent accountability | ✅ Active |
| 06 | **Network Recon** | NDSS 2026 | eBPF-backed network reconnaissance with formal admission control | ✅ Active |
| 07 | **Malware Triage** | RAID 2026 | Statistical reconstruction of malware triage decisions | ✅ Active |
| 08 | **File Inclusion** | ASIACCS 2026 | Provenance-tracked file inclusion for agent workflows | ✅ Active |
| 09 | **MITM Interception** | ESORICS 2026 | Ephemeral buffer interception for credential extraction detection | ✅ Active |
| 10 | **Vulnerability Assessment** | ACSAC 2026 | Cross-vendor vulnerability scanning with authoritative taxonomy | ✅ Active |
| 11 | **Degenerate Reporting** | RAID 2026 | Meta-science audit: evaluations that cannot rule out do-nothing policies | ✅ Active |
| 12 | **Provenance-Bound Authorization** | SACMAT 2027 | Provenance-aware authorization for untrusted calendar content | ✅ Active |

Each demo is a **self-contained, reproducible research artifact** with:
- 📦 Frozen dependencies & environment specifications
- 📊 Pre-computed evidence packages (JSON)
- 🧪 Comprehensive test suites (≥90% coverage)
- 📄 Venue-aligned documentation & claim ledgers
- 🔬 Statistical validation scripts

---

## ⚙️ Installation

### Unified Installation (All Demos)
```bash
pip install agentic-security-demos[all]
```

### Individual Demo Installation
```bash
# Install specific demo
pip install agentic-security-demos[demo-01]   # Blind Verification
pip install agentic-security-demos[demo-02]   # Supply Chain AIBOM
pip install agentic-security-demos[demo-03]   # Eval Design Invariants
pip install agentic-security-demos[demo-04]   # Prompt Injection
pip install agentic-security-demos[demo-05]   # Evidence Release
pip install agentic-security-demos[demo-06]   # Network Recon
pip install agentic-security-demos[demo-07]   # Malware Triage
pip install agentic-security-demos[demo-08]   # File Inclusion
pip install agentic-security-demos[demo-09]   # MITM Interception
pip install agentic-security-demos[demo-10]   # Vuln Assessment
pip install agentic-security-demos[demo-11]   # Degenerate Reporting
pip install agentic-security-demos[demo-12]   # Provenance-Bound Authz
```

### Development Installation
```bash
git clone https://github.com/radanliev/agentic-security-demos.git
cd agentic-security-demos
pip install -e ".[dev,all]"
```

### Verify Installation
```bash
# Run smoke tests for all demos
agentic-security-demos --smoke-test

# List available demos
agentic-security-demos --list-demos
```

---

## 🚀 Quick Start

### Run a Complete Demo Pipeline
```bash
# Demo 1: Blind Verification (SATML)
cd demo-01-blind-verification
python -m demo.run_full_pipeline --config configs/satml_submission.yaml

# Demo 4: Prompt Injection Authority (IEEE SP)
cd demo-04-prompt-injection
python -m authoritybound.run_assessment --model gpt-4 --attacks all

# Demo 7: Malware Triage (RAID)
cd demo-07-malware-triage
python -m triage_trap.run_route_s --challenge-battery v3
```

### Generate Evidence Packages
```bash
# Produce frozen evidence for any demo
agentic-security-demos evidence generate --demo 01 --output ./evidence/

# Verify evidence integrity
agentic-security-demos evidence verify --input ./evidence/
```

### Reproduce Paper Results
```bash
# Reproduce all paper claims from frozen evidence
agentic-security-demos reproduce --paper satml2026 --evidence-dir ./evidence/
```

---

## 🔬 Reproducibility

All demos follow the **Agentic Security Reproducibility Standard**:

| Guarantee | Mechanism |
|-----------|-----------|
| **Environment Freeze** | `requirements.lock` + `conda-lock.yml` + Docker images |
| **Evidence Immutability** | SHA-256 sealed evidence packages on Zenodo |
| **Statistical Rigor** | Pre-registered analysis plans with p-value correction |
| **Compute Transparency** | GPU-hours logged; CPU fallback documented |
| **Adversarial Robustness** | Seeded RNG; deterministic attack ordering |

### Reproducibility Checklist
- [ ] Clone repo at tagged release
- [ ] Install exact dependencies: `pip install -r requirements.lock`
- [ ] Download evidence from Zenodo (DOI in `CHANGELOG.md`)
- [ ] Run: `agentic-security-demos reproduce --all`
- [ ] Compare outputs to `results/reference/`

---

## 🏛️ Venues & Publications

| Demo | Venue | Year | Paper | Artifact |
|------|-------|------|-------|----------|
| 01 | SATML | 2027 | [Blind Verification](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 02 | CCS | 2027 | [AIBOM Drift](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 03 | NeurIPS | 2027 | [Eval Invariants](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 04 | IEEE SP | 2027 | [Tool Authority](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 05 | USENIX Security | 2027 | [Evidence Assurance](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 06 | NDSS | 2028 | [Network Recon](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 07 | RAID | 2027 | [Malware Triage](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 08 | ASIACCS | 2027 | [File Inclusion](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 09 | ESORICS | 2027 | [MITM Interception](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 10 | ACSAC | 2027 | [Vuln Assessment](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 11 | RAID | 2027 | [Degenerate Reporting](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |
| 12 | SACMAT | 2027 | [Provenance-Bound Authz](https://arxiv.org/abs/XXXX.XXXXX) | [Zenodo](https://zenodo.org/records/XXXXXXX) |

---

## 📖 Citation

If you use this collection in your research, please cite:

```bibtex
@misc{radanliev2026agenticsecuritydemos,
  title={Agentic AI Security Demos: A Reproducible Collection for Top-Tier Venues},
  author={Radanliev, Petar},
  year={2026},
  publisher={GitHub},
  journal={GitHub Repository},
  howpublished={\url{https://github.com/radanliev/agentic-security-demos}},
  doi={10.5281/zenodo.XXXXXXX}
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
- **Anonymous reviewers** at SATML, CCS, NeurIPS, IEEE SP, USENIX, NDSS, RAID, ASIACCS, ESORICS, ACSAC, SACMAT
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