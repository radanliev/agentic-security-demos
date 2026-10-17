# Author Cover Letter — The Web Conference 2027 (WWW'27)

**To**: Program Committee Co-Chairs and Track Chairs  
**Conference**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)  
**Track**: Research Track — Web Infrastructure and Agentic Systems  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)

---

## Submission Details

- **Title**: Status 200 Is Not a File: A Validated Census of the Agent-Facing Web in Common Crawl
- **Track**: Research Track — Web Infrastructure and Agentic Systems
- **Keywords**: agent-facing web, llms.txt, Common Crawl, robots.txt, prompt injection, web measurement, dual governance, autonomous agents
- **Submission Type**: Full Research Paper (ACM SIGCONF format, 8 pages main text, up to 12 pages total)

---

## Abstract

The Web research question is whether an HTTP success stored under an agent-facing path is evidence that a site publishes an agent file. Conventions such as /llms.txt give language-model agents a Markdown entry point to a website, and adoption is increasingly measured from web-crawl indices, where an HTTP 200 record at the path is counted as adoption. This paper tests that inference at full scale on Common Crawl. A walk of columnar index partitions of CC-MAIN-2026-39 finds that the crawler requested /llms.txt on 16,029 hosts, of which the majority answered 200. A seeded sample of registered domains, stratified by Tranco tier and classified from archived bytes, shows that the 200 status is frequently an HTML soft-404: 112 of 211 cached responses are soft-404s, while only 67 are conformant agent files. The soft-404 gate is validated against live random-path probes, homepage similarity, and Common Crawl MIME detection, agreeing with independent human validation. Correcting for soft-404s substantially lowers naive adoption rates. Furthermore, crawler frontier bias understates live adoption. Usable files remain small, predominantly platform-generated, and often contain broken links. We release our open-source classification gate, stratified sample, and annotation protocol to establish rigorous standards for agent-facing web measurement.

---

## Author & Anonymous Statement

This manuscript is submitted under the mandatory double-blind review policy of The Web Conference 2027. In compliance with the conference guidelines:
1. All author names, institutional affiliations, and direct identifiers have been omitted from the manuscript and supplementary materials.
2. Any referenced codebase, raw crawl indices, and experimental validation logs are provided via anonymised repositories without identifying git commit author metadata.
3. The research questions explicitly investigate a core Web infrastructure challenge: empirical measurement, protocol conformance, and failure modes of agent-facing endpoints (/llms.txt) in the global Web crawl.

---

## OpenReview Intent & Author Cap Compliance

The authors formally declare the intent to register this submission on the official OpenReview portal by the abstract registration deadline of **18 October 2026 23:59 AoE**, followed by final PDF upload before **25 October 2026 23:59 AoE**. 

Furthermore, all listed authors comply with the WWW'27 author cap policy (no author exceeds the maximum limit of seven research-track submissions across the conference).

---

## Dual Submission Declaration

This manuscript presents original, unpublished work. It has not been published elsewhere, nor is it concurrently submitted or under active consideration at any other conference, journal, or workshop. Post-rejection sequential fallbacks (Option B: WWW'27 Short Paper / IMC'27, or Option C: IMC'27) will only be activated in the event of an explicit rejection decision from WWW'27.
