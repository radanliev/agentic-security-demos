# Responsible Use Policy

## Purpose

These materials teach **defensive security concepts** for agentic AI systems using **safe, local simulations only**.

## Mandatory Rules

### 1. No External Targeting
- Never run demos against public IP addresses, domains, or services
- Never scan systems you do not own or have explicit written permission to test
- All fixtures are synthetic; treat them as such

### 2. No Real Credentials
- Never use real API keys, passwords, tokens, or private keys
- Demo keys are generated at runtime and marked `DEMO_KEY_*`
- Delete generated keys after each session

### 3. No Malware Execution
- Synthetic PCAP/metadata fixtures are **inert data only**
- Never execute, interpret, or feed unknown binaries to any tool
- "Quarantine" in demos means moving a JSON record, not a file

### 4. No Research Misrepresentation
- Teaching results are **demonstrations/placeholders**, not validated research
- Always label outputs: `"notes": "Synthetic teaching fixture"`
- Do not cite demo outputs as experimental evidence

### 5. Scope Confinement
- Each demo documents its operational boundaries
- Stay within `localhost`, synthetic fixtures, and local containers
- Do not adapt demos for production use without expert review

## For Instructors

- Verify student environments are isolated (no internet in CI/lab)
- Review student forks before merging PRs
- Emphasize the simulation vs. reality distinction in lectures

## For Students

- Ask before deviating from provided fixtures
- Report any accidental external connection immediately
- Document all runs with seed, commit, environment, command

## Violation Consequences

- Course-level: per instructor policy
- Repository-level: PR rejection, issue closure, access restriction
- Legal: unauthorized scanning/testing may violate CFAA and local laws

## Acknowledgment

By using this repository, you acknowledge these rules and accept responsibility for your actions.