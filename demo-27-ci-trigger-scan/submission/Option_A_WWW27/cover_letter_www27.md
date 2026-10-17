# Author Cover Letter — The Web Conference 2027 (WWW'27)

**To**: Program Committee Co-Chairs and Track Chairs  
**Conference**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)  
**Track**: Research Track — Web Infrastructure and Agentic Systems  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)

---

## Submission Details

- **Title**: Trust Me, I'm an Issue: Measuring the Prompt-Injection Exposure of AI Coding Agents Wired to Public Issue Trackers
- **Track**: Research Track — Web Infrastructure and Agentic Systems
- **Keywords**: Web security, delegated authority, AI coding agents, continuous integration, indirect prompt injection, software supply chain, confused deputy
- **Submission Type**: Full Research Paper (ACM SIGCONF format, 8 content pages, up to 12 pages total including references and appendices)

---

## Abstract

Public code forges are foundational Web collaboration platforms where open issue trackers and pull-request dialogues accept untrusted input from arbitrary Web accounts. When repository maintainers automate autonomous AI coding agents by wiring them to forge webhook events, does the platform delegate privileged write authority to an unauthenticated Web adversary? This paper presents an empirical measurement of delegated authority and prompt-injection reachability across AI coding agents deployed in continuous integration (CI) workflows. A stored-file census across 367 agent repositories and 448 workflows reveals that 67.0% execute on untrusted Web triggers (issues, pull_request, pull_request_target), with 88.3% granting write-capable permissions (contents:write or pull-requests:write). Syntactic reachability analysis indicates that 95.8% of untrusted-trigger repositories omit maintainer identity or collaborator gates, leaving 64.2% of all repositories delegating write tokens upon arbitrary Web issue creation. Upstream vendor documentation heavily influences exposure: where starter templates omit perimeter gating (e.g., Anthropic Claude Code), 86.8% of downstream adoptions remain ungated, whereas default-gated templates (e.g., Google Gemini CLI) achieve 100% gated adoptions. A capability-coverage model indicates that defense-in-depth combining split-token read-only sandboxes with identity gating eliminates 96.0% of attack toolpaths while preserving 100% benign developer utility.

---

## Author & Anonymous Statement

This manuscript is prepared under the mandatory double-blind review policy of The Web Conference 2027:
1. All author names, institutional affiliations, and direct acknowledgments are omitted from the manuscript and supplementary files.
2. The empirical study investigates a fundamental Web infrastructure challenge: how unauthenticated Web inputs to public code forges propagate into delegated write actions by autonomous Web agents.
3. Code repositories, evaluation scripts, and workflow corpora are shared via anonymised repositories without identifying git commit metadata or institutional identifiers.
4. Prior work by the authors is cited in the third person.

---

## OpenReview Intent & Author Cap Compliance

The authors formally record their intent to register the abstract on the OpenReview submission portal by the deadline of **18 October 2026 23:59 AoE**, followed by final paper upload prior to **25 October 2026 23:59 AoE**.

All contributing authors comply with the WWW'27 author cap policy, confirming that no author exceeds seven (7) submissions to the research track.

---

## Dual Submission Policy Declaration

This manuscript presents original, unpublished empirical research. It has not been published elsewhere, nor is it concurrently submitted to or under active consideration by any other conference, journal, or workshop. Sequential post-rejection options (Plan B via Black Hat USA / Arsenal, Plan C via DEF CON Demo Labs) remain strictly dormant and will not be activated unless an explicit rejection notification is received from WWW'27.
