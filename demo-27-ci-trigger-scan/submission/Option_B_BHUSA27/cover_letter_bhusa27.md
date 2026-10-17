# Author Cover Letter — Black Hat USA 2027 (Briefings & Arsenal)

**To**: Black Hat USA Review Board and Arsenal Selection Committee  
**Conference**: Black Hat USA 2027, Mandalay Bay, Las Vegas, NV (August 2027)  
**Tracks**: Briefings (Application Security / Software Supply Chain) and Black Hat Arsenal (Open Source Security Tools)  
**Submission Portal**: Black Hat CFP Portal (`https://www.blackhat.com/us-27/call-for-papers.html`)

---

## Submission Details

- **Title**: Trust Me, I'm an Issue: Weaponising and Remediating Prompt-Injection Exposure in CI Coding Agents
- **Tool Name**: `CI-Trigger-Scan` (Zero-dependency static security scanner for agentic CI workflows)
- **Primary Topic**: AI Agent Security, Continuous Integration (CI/CD) Security, Confused Deputy Exploitation, Software Supply Chain
- **Presentation Format**: 50-minute Briefing presentation with live interactive Arsenal tool demonstration

---

## Executive Summary & Abstract

AI coding agents deployed across continuous integration (CI) workflows are transforming repository automation, but they introduce a severe Confused Deputy vulnerability: delegating write-capable forge tokens to unauthenticated Web actors. When a repository wires autonomous agents to open webhook events—such as public issues, pull requests, and discussions—without strict perimeter gating, any outsider can inject prompt payloads that compel the agent to execute arbitrary tools. In this briefing and Arsenal tool demonstration, we unveil CI-Trigger-Scan, an automated open-source security scanner designed to detect vulnerable agent workflow wiring. Drawing on an empirical census of 367 agent repositories and 448 workflows, we show that 67.0% execute on untrusted Web triggers and 88.3% grant write permissions, with 95.8% omitting maintainer identity checks. We demonstrate live exploit mechanics: weaponising public issues to force coding agents to dump CI secrets, modify production source branches, and compromise downstream releases. We dissect how default starter templates published by AI vendors (such as Anthropic Claude Code) propagate ungated configurations to 86.8% of downstream adoptions, contrasting them with secure-by-default patterns. Finally, we demonstrate practical defenses: implementing identity-verified perimeter gating and split-token sandboxing that neutralises 96.0% of attack paths while preserving developer utility.

---

## Why Black Hat Attendees Must Hear This

Repository maintainers and enterprise devsecops teams are aggressively adopting agentic CI assistants without understanding the fundamental boundary collapse involved in wiring unauthenticated public forge webhooks to privileged runners. 
1. **Novel Vulnerability Class**: We formalise and demonstrate the Confused Deputy hazard in agentic CI pipelines.
2. **Actionable Open-Source Tool**: Attendees and maintainers receive `CI-Trigger-Scan` to immediately audit their organisation's GitHub Actions and GitLab CI workflows.
3. **Upstream Supply Chain Accountability**: We highlight the direct empirical correlation between vendor starter documentation and enterprise vulnerability rates.

---

## Live Demonstration Outline

- **Arsenal Station**: Continuous live scanning of participant-supplied repository URLs and YAML workflows using `CI-Trigger-Scan`.
- **Briefing Demo**: A controlled sandbox showing a live indirect prompt injection via a simulated GitHub issue that attempts to hijack runner credentials, contrasted immediately with the perimeter-gated, split-token defense architecture blocking the attack.

---

## Sequential Activation Policy

This submission packet serves as **Plan B** for Demo 27. It remains strictly dormant while Plan A is under evaluation at The Web Conference 2027 (notification 04 January 2027). In accordance with dual-submission ethics, this proposal will be activated only in the event of an explicit rejection from WWW'27, months before the Black Hat CFP deadline in May 2027.
