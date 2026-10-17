# Author Cover Letter — WWW'27 Short Paper / IMC'27

**To**: Program Committee Co-Chairs and Track Chairs  
**Venue Options**: 
1. The Web Conference 2027 (WWW'27) — Short Papers Track (Deadline: 16 November 2026 AoE)
2. ACM Internet Measurement Conference 2027 (IMC'27) — Short / Measurement Track
**Track**: Web Measurement, Infrastructure, and Autonomous Systems  

---

## Submission Details

- **Title**: Status 200 Is Not a File: Measuring Soft-404 Fallback and Frontier Bias in Agent Web Censuses
- **Submission Type**: Short Research Paper / Measurement Paper (ACM SIGCONF format, 4–6 pages)
- **Keywords**: agent-facing web, llms.txt, Common Crawl, web measurement, soft-404, crawler frontier

---

## Abstract

Conventions such as /llms.txt propose Markdown entry points for web-browsing autonomous agents, with adoption widely estimated by counting HTTP 200 responses in web-crawl indices. In this measurement short paper, we demonstrate that HTTP status 200 is not reliable evidence of an agent-facing file. Evaluating Common Crawl CC-MAIN-2026-39 index partitions alongside archived WARC response bytes across Tranco-stratified domains reveals that the majority of stored 200 responses are in fact HTML soft-404 error pages: across 211 cached responses, 112 are soft-404s and only 67 are conformant agent files. We introduce an automated multi-cue soft-404 detection gate validated against homepage similarity, MIME analysis, and independent human annotations. Applying this filter dramatically deflates headline adoption metrics across top-tier domains. Simultaneously, comparison with crawler-independent live probes demonstrates that Common Crawl's crawl frontier significantly under-samples the long tail of genuine adopters. We release our measurement pipeline, classification filters, and stratified benchmarks to enable methodologically sound longitudinal tracking of the emerging agent-facing web.

---

## Author & Anonymous Statement

This manuscript is submitted under the double-blind review policy. In compliance with venue instructions:
1. All author identities, affiliations, and institutional references are strictly omitted from the text and metadata.
2. Code repositories and data artifacts are provided via anonymised hosting services.
3. The measurement focus investigates empirical discrepancies between naive HTTP status codes and validated web payloads for agent conventions.

---

## Sequential Fallback & Policy Statement

This submission package serves as **Plan B** for Demo 20 (`agent-web-census`):
- It remains strictly **dormant** while the full research paper is under consideration at WWW'27 Research Track (Plan A).
- Activation occurs sequentially: either if Plan A is redirected to the short paper track (deadline 16 November 2026), or upon formal rejection of Plan A (scheduled for 04 January 2027) targeting IMC'27.
- Under no circumstances will this manuscript be submitted concurrently while under review elsewhere.
