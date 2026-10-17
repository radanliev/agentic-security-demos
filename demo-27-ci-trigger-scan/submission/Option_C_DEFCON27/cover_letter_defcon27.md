# Author Cover Letter — DEF CON 35 Demo Labs

**To**: DEF CON 35 Demo Labs Selection Committee  
**Event**: DEF CON 35, Las Vegas, NV (August 2027)  
**Track**: Demo Labs  
**Submission Portal**: DEF CON CFP Portal (`https://defcon.org/html/defcon-35/dc-35-cfp.html`)

---

## Submission Details

- **Station Title**: CI-Trigger-Scan: Hunting Confused Deputies in Agentic CI Pipelines
- **Tool Name**: `CI-Trigger-Scan`
- **Topic**: CI/CD Security, AI Coding Agents, Indirect Prompt Injection, Confused Deputy Exploits
- **Format**: Interactive Demo Labs Station (Hands-on demonstrations, BYOR live scanning, interactive breakout exercises)
- **Licence**: Open Source (MIT License)

---

## Station Abstract & Description

Wiring autonomous AI coding agents directly to public GitHub issue trackers creates an open Confused Deputy vulnerability: unauthenticated Web users can issue prompts that trigger privileged CI runners to execute arbitrary tools and steal write tokens. At DEF CON 35 Demo Labs, we present CI-Trigger-Scan, an open-source security tool that parses workflow definitions to identify vulnerable public-trigger and write-permission wiring. Based on our real-world census of 367 agent repositories, 64.2% of surveyed repositories delegate write tokens to unauthenticated issue creators without maintainer review. At our interactive Demo Labs station, attendees can run live audits against their own repositories, test simulated indirect prompt injections in a safe offline sandbox, and learn how to deploy fail-closed perimeter gating and split-token sandboxes that neutralise 96.0% of attack paths while keeping agents useful.

---

## Interactive Experience for DEF CON Attendees

1. **Live Repository Auditing (BYOR)**: Attendees can clone or provide URLs for their own GitHub repositories to inspect their GitHub Actions agent configurations in seconds.
2. **Interactive Exploit Simulator**: Hands-on challenge where attendees attempt to craft issue payloads that trigger simulated tokens in a local offline sandbox.
3. **Remediation Workshop**: Attendees receive ready-to-merge YAML templates that enforce fail-closed perimeter gates (`author_association`) and split-token sandboxes.

---

## Sequential Activation Policy

This package serves as **Plan C** for Demo 27. It remains dormant during the review cycle of Plan A (WWW'27) and Plan B (Black Hat USA 2027). Activation is triggered only if earlier options are not pursued, well in advance of the DEF CON Demo Labs CFP deadline in June 2027.
