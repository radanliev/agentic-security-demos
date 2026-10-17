# Author Cover Letter — The Web Conference 2027 (WWW'27)

**To**: Program Committee Co-Chairs and Track Chairs  
**Conference**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)  
**Track**: Research Track — Security and Privacy  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)

---

## Submission Details

- **Title**: Connecting Agents to Web Services: HTTP Endpoints, Secret Headers and Version Changes in the Model Context Protocol Registry
- **Track**: Research Track — Security and Privacy
- **Keywords**: Model Context Protocol, agentic systems, Web measurement, tool poisoning, HTTP endpoints, provenance attestations
- **Submission Type**: Full Research Paper (ACM SIGCONF format, 8 pages main text, up to 12 pages total)

---

## Abstract

The official Model Context Protocol (MCP) registry walk of 30 September 2026 contains 126,847 version records across 37,815 servers, of which 61.89% declare remote HTTP endpoints and 56.96% operate purely as remote services without installable packages. This census measures the emerging protocol connecting autonomous agents to web services. Remote endpoints resolve to 15,738 distinct hosts across 6,432 registrable domains, with 79.5% unranked in the Tranco Top-1M. Furthermore, 3,679 remotes declare confidential headers marked isSecret, binding ambient credentials to outbound requests. Across 89,032 publication-ordered version transitions, releases arrive rapidly (median 0.8 days, 52.4% within 24 hours). Transitions modify remote URLs in 1,353 cases: 52.4% alter destination hostnames, 36.1% cross administrative eTLD+1 boundaries, and 69.8% of cross-domain migrations target multi-tenant serverless or PaaS platforms. Evaluating a deterministic pattern screen over 40,672 tool descriptions yields a 1.25% flag rate; on MCPTox attacks, it achieves only 6.2% recall while flagging benign documentation in 89.2% of real-world hits. Rather than claiming unverified attack prevalence, the paper quantifies longitudinal structural shifts and proposes three architectural defences---origin-bound credential scoping, manifest attestations, and domain lifecycle verification---to secure agentic web interfaces.

---

## Author & Anonymous Statement

This manuscript is submitted under the mandatory double-blind review policy of The Web Conference 2027. In compliance with the conference guidelines:
1. All author names, institutional affiliations, and direct identifiers have been omitted from the manuscript and supplementary materials.
2. Any referenced codebase and experimental logs are provided via anonymised repositories without identifying git commit author metadata.
3. The research questions explicitly investigate a core Web infrastructure problem: remote HTTP tool endpoints, secret headers, and version migrations across the Model Context Protocol ecosystem connecting autonomous agents to web services.

---

## OpenReview Intent & Author Cap Compliance

The authors formally declare the intent to register this submission on the official OpenReview portal by the abstract registration deadline of **18 October 2026 23:59 AoE**, followed by final PDF upload before **25 October 2026 23:59 AoE**.

Furthermore, all listed authors comply with the WWW'27 author cap policy (no author exceeds the maximum limit of seven research-track submissions across the conference).

---

## Dual Submission Declaration

This manuscript presents original, unpublished work. It has not been published elsewhere, nor is it concurrently submitted or under active consideration at any other conference, journal, or workshop. Post-rejection sequential fallbacks (Plan B: IMC'27, Plan C: AsiaCCS'28) will only be activated in the event of an explicit rejection decision from WWW'27.
