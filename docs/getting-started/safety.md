# Safety First

## ⚠️ Mandatory Reading

**Before running any demo, you MUST read and acknowledge:**

1. [RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md) — Mandatory safety rules
2. [SECURITY.md](../SECURITY.md) — Vulnerability reporting
3. Each demo's README Safety Notice section

## Safety Guarantees

| Property | Guarantee | Verification |
|----------|-----------|--------------|
| **Network access** | **None** | `make verify-safety` checks imports |
| **Credentials** | **None** | `make verify-safety` scans for keys |
| **Malware** | **None** | Synthetic fixtures only |
| **Private data** | **None** | No research datasets |

## Mandatory Rules

### 1. No External Targeting
- Never run demos against public IPs, domains, or services
- Never scan systems you don't own
- All fixtures are synthetic; treat them as such

### 2. No Real Credentials
- Never use real API keys, passwords, tokens
- Demo keys are generated at runtime (`DEMO_KEY_*`)
- Delete generated keys after each session

### 3. No Malware Execution
- Synthetic PCAP/metadata fixtures are **inert data only**
- Never execute, interpret, or feed unknown binaries
- "Quarantine" in demos = moving a JSON record, not a file

### 4. No Research Misrepresentation
- Teaching results are **demonstrations/placeholders**
- Always label outputs: `"notes": "Synthetic teaching fixture"`
- Do not cite demo outputs as experimental evidence

### 5. Scope Confinement
- Each demo documents its operational boundaries
- Stay within `localhost`, synthetic fixtures, local containers
- Do not adapt demos for production use without expert review

## Violation Consequences

| Level | Consequence |
|-------|-------------|
| Course | Per instructor policy |
| Repository | PR rejection, issue closure, access restriction |
| Legal | Unauthorized scanning/testing may violate CFAA and local laws |

## Acknowledgment

By using this repository, you acknowledge these rules and accept responsibility for your actions.

---

**Remember**: These materials teach **defensive concepts** using **safe simulations only**. The goal is to learn how to build secure agentic systems — not to attack real systems.