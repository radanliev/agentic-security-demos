# Agentic Security Demos

[![CI](https://github.com/agentic-security-demos/agentic-security-demos/workflows/CI/badge.svg)](https://github.com/agentic-security-demos/agentic-security-demos/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: Educational](https://img.shields.io/badge/status-educational-green.svg)]()
[![Safety: Offline Only](https://img.shields.io/badge/safety-offline%20only-blue.svg)]()

A collection of **10 educational modules** for teaching security concepts in agentic AI systems. All demonstrations use **local synthetic fixtures only** — no live network access, real credentials, malware, or private data.

## 🎯 Learning Objectives

| Demo | Topic | Key Concepts |
|------|-------|--------------|
| [01](demo-01-blind-verification/) | Blind Verification | Commitment-before-test, oracle evaluation, post-hoc insufficiency |
| [02](demo-02-supply-chain-aibom/) | AIBOM Drift Detection | Component inventory, policy gates, waiver mechanisms |
| [03](demo-03-eval-invariants/) | Evaluation Invariants | Leakage detection, difficulty calibration, stability, reproducibility |
| [04](demo-04-authoritybound/) | Authority Confinement | Confused deputy, provenance tracking, capability tokens |
| [05](demo-05-eviassure/) | Evidence-Backed Release | Hash chains, Merkle trees, inclusion proofs, fail-closed gates |
| [06](demo-06-reconscope/) | Network Recon Safety | Protocol parsing, provenance labels, scope enforcement |
| [07](demo-07-triagetrap/) | Safe Malware Triage | Provenance tracking, base-rate awareness, injection detection |
| [08](demo-08-inclusiontrap/) | File Inclusion Boundaries | LFI/RFI simulation, scope enforcement, authority separation |
| [09](demo-09-interceptbound/) | Traffic Interception & Taint | Taint tracking, ephemeral buffers, downstream action guards |
| [10](demo-10-scanbound/) | Vulnerability Scan Control | Scope validation, check validation, taint-aware actions |

## 🚀 Quick Start

```bash
# Clone and enter
git clone https://github.com/agentic-security-demos/agentic-security-demos.git
cd agentic-security-demos

# One-time setup (installs dependencies, generates fixtures)
make setup

# Run all tests (safe, offline, deterministic)
make test

# Run a specific demo (replace 01 with 02-10)
make demo DEMO=01
```

## 📁 Repository Structure

```
agentic-security-demos/
├── demo-01-blind-verification/      # Blind commitment & oracle evaluation
├── demo-02-supply-chain-aibom/      # AIBOM drift detection & policy gates
├── demo-03-eval-invariants/         # Evaluation invariants (5 checks)
├── demo-04-authoritybound/          # Confused deputy & authority confinement
├── demo-05-eviassure/               # Cryptographic evidence pipelines
├── demo-06-reconscope/              # Network recon with provenance
├── demo-07-triagetrap/              # Safe malware triage (synthetic only)
├── demo-08-inclusiontrap/           # File inclusion & scope boundaries
├── demo-09-interceptbound/          # Traffic interception & taint tracking
├── demo-10-scanbound/               # Vulnerability assessment scope control
├── shared/                          # Shared utilities (result schema, reproducibility)
├── docs/                            # Documentation
├── examples/                        # Cross-demo examples
├── .github/
│   ├── workflows/ci.yml             # CI: offline tests only
│   ├── ISSUE_TEMPLATE/              # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md     # PR template
├── Makefile                         # Root commands (setup, test, demo)
├── pyproject.toml                   # Project metadata
├── requirements.txt                 # Python dependencies
├── LICENSE                          # MIT License
├── CONTRIBUTING.md                  # Contribution guidelines
├── CODE_OF_CONDUCT.md               # Code of Conduct
├── SECURITY.md                      # Security policy
├── RESPONSIBLE_USE.md               # Responsible use policy
├── CHANGELOG.md                     # Version history
├── CITATION.cff                     # Citation metadata
└── .github/dependabot.yml           # Dependency updates
```

## 🛡️ Safety Guarantees

| Property | Guarantee |
|----------|-----------|
| **Network access** | **None** — all fixtures are local synthetic data |
| **Credentials** | **None** — only disposable demo keys generated at runtime |
| **Malware** | **None** — only inert synthetic metadata and canaries |
| **Private data** | **None** — no research datasets, API keys, or participant data |
| **External dependencies** | **Minimal** — standard library + `pytest`, `pyyaml`, `cryptography` |

Every test runs in a hermetic environment with no network access.

## 📚 Educational Use

- **Level**: Undergraduate / Master's CS
- **Prerequisites**: Basic Python, security awareness
- **Time per demo**: 30-60 minutes
- **Exercises**: Beginner / Standard / Extension per demo

## 🔬 Reproducibility

Every demo run produces a standardized JSON result:

```json
{
  "demo": "demo-01-blind-verification",
  "experiment": "comparison",
  "seed": 42,
  "commit": "abc1234",
  "environment": "Python 3.11, Ubuntu 22.04",
  "command": "make demo DEMO=01",
  "result": "pass",
  "notes": "Synthetic teaching fixture"
}
```

Record these fields in lab reports. **Teaching results are demonstrations, not validated research claims.**

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding exercises or improving explanations
- Fixing bugs in starter code or tests
- Enhancing reproducibility
- Adding new demos (following the established pattern)

## 📖 Citation

If you use these materials in teaching or research, please cite:

```bibtex
@software{agentic-security-demos,
  title = {Agentic Security Demos: Teaching Modules for Agentic AI Security},
  author = {Agentic Security Demos Contributors},
  year = {2024},
  url = {https://github.com/agentic-security-demos/agentic-security-demos},
  note = {Educational materials for teaching agentic AI security concepts}
}
```

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

## ⚠️ Responsible Use

**Critical**: These modules teach **defensive concepts** using **safe simulations only**.
- Do NOT target public systems, real services, or third-party infrastructure
- Do NOT use real credentials, API keys, or private keys
- Do NOT execute unknown code or malware samples
- Do NOT present teaching results as peer-reviewed research findings

See [RESPONSIBLE_USE.md](RESPONSIBLE_USE.md) and [SECURITY.md](SECURITY.md) for full policies.

## 🙋 Support

- **Issues**: [GitHub Issues](https://github.com/agentic-security-demos/agentic-security-demos/issues)
- **Discussions**: [GitHub Discussions](https://github.com/agentic-security-demos/agentic-security-demos/discussions)
- **Security**: See [SECURITY.md](SECURITY.md) for vulnerability reporting

---

**Keywords**: agentic AI, AI security, LLM security, autonomous agents, security education, teaching materials, blind verification, AIBOM, supply chain security, evaluation invariants, authority confinement, confused deputy, evidence-backed release, network reconnaissance, malware triage, file inclusion, traffic interception, vulnerability scanning, synthetic fixtures, reproducible evaluation