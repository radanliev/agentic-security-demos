# Agentic Security Demos

[![CI](https://github.com/agentic-security-demos/agentic-security-demos/workflows/CI/badge.svg)](https://github.com/agentic-security-demos/agentic-security-demos/actions/workflows/ci.yml)
[![Docs](https://github.com/agentic-security-demos/agentic-security-demos/workflows/Deploy%20Documentation/badge.svg)](https://agentic-security-demos.github.io/agentic-security-demos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Educational modules for teaching agentic AI security concepts**

All demonstrations use **local synthetic fixtures only** — no live network access, real credentials, malware, or private data.

---

## 🎯 Quick Start

```bash
# Clone and enter
git clone https://github.com/agentic-security-demos/agentic-security-demos.git
cd agentic-security-demos

# One-time setup
make setup

# Run all tests (316 tests, safe, offline, deterministic)
make test

# Run a specific demo (01-10)
make demo DEMO=01
```

---

## 📚 Demos Overview

| # | Demo | Topic | Key Concepts | Difficulty |
|---|------|-------|--------------|------------|
| 01 | [Blind Verification](demos/01-blind-verification.md) | Commitment before test | Blind commitment, oracle evaluation, post-hoc insufficiency | ⭐⭐ |
| 02 | [Supply Chain AIBOM](demos/02-supply-chain-aibom.md) | Drift detection | Component inventory, policy gates, waiver mechanisms | ⭐⭐ |
| 03 | [Evaluation Invariants](demos/03-eval-invariants.md) | Robust evaluation | Leakage detection, difficulty calibration, stability | ⭐⭐⭐ |
| 04 | [Authority Bound](demos/04-authoritybound.md) | Confused deputy | Provenance tracking, capability tokens, scope enforcement | ⭐⭐⭐ |
| 05 | [Evidence Assurance](demos/05-eviassure.md) | Cryptographic evidence | Hash chains, Merkle trees, inclusion proofs, fail-closed gates | ⭐⭐⭐ |
| 06 | [ReconScope](demos/06-reconscope.md) | Network recon safety | Protocol parsing, provenance labels, scope enforcement | ⭐⭐ |
| 07 | [TriageTrap](demos/07-triagetrap.md) | Safe malware triage | Provenance tracking, base-rate awareness, injection detection | ⭐⭐ |
| 08 | [InclusionTrap](demos/08-inclusiontrap.md) | File inclusion boundaries | LFI/RFI simulation, scope enforcement, authority separation | ⭐⭐⭐ |
| 09 | [InterceptBound](demos/09-interceptbound.md) | Traffic interception | Taint tracking, ephemeral buffers, downstream action guards | ⭐⭐⭐ |
| 10 | [ScanBound](demos/10-scanbound.md) | Vuln scan control | Scope validation, check validation, taint-aware actions | ⭐⭐⭐ |

---

## 🛡️ Safety Guarantees

| Property | Guarantee |
|----------|-----------|
| **Network access** | **None** — all fixtures are local synthetic data |
| **Credentials** | **None** — only `DEMO_KEY_*` generated at runtime |
| **Malware** | **None** — inert synthetic metadata only |
| **Private data** | **None** — no research datasets, API keys, or participant data |

---

## 📖 Learning Path

| Level | Recommended Demos | Time |
|-------|-------------------|------|
| **Beginner** | 01, 02, 06, 07 | 2-3 hrs |
| **Intermediate** | 03, 04, 08, 09 | 3-4 hrs |
| **Advanced** | 05, 10 | 2-3 hrs |

---

## 🤝 Community

- 💬 [Discussions](https://github.com/agentic-security-demos/agentic-security-demos/discussions) - Questions, ideas, show-and-tell
- 🐛 [Issues](https://github.com/agentic-security-demos/agentic-security-demos/issues) - Bugs, features, docs
- 🤝 [Contributing](contributing/guidelines.md) - How to contribute
- 🛡️ [Safety](RESPONSIBLE_USE.md) - Mandatory safety rules

---

## 📄 License

MIT License — see [LICENSE](about/license.md) for details.

---

*Built with ❤️ for AI security education*