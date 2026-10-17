# Author Cover Letter — ACM Internet Measurement Conference 2027 (IMC'27)

**To**: Program Committee Co-Chairs  
**Conference**: ACM Internet Measurement Conference 2027 (IMC'27)  
**Submission Category**: Research / Measurement Paper  
**Submission Portal**: HotCRP / OpenReview (per IMC'27 CFP)

---

## Submission Details

- **Title**: Status 200 Is Not a File: An Empirical Measurement Study of the Agent-Facing Web in Common Crawl
- **Keywords**: web measurement, agent-facing web, llms.txt, Common Crawl, soft-404, internet measurement, crawler frontier bias
- **Submission Type**: Full Research Paper (ACM format, up to 13 pages excluding references/appendix)

---

## Abstract

Large-scale empirical measurement of agent-facing web infrastructure—such as /llms.txt manifests intended for autonomous LLM agents—faces severe methodological pitfalls when relying on passive crawl indices. In this paper, we conduct a comprehensive measurement study of agent-facing web endpoints across Common Crawl (CC-MAIN-2026-39 and CC-MAIN-2026-30) and the Tranco Top 1M list. We find that naive index-based measurements fundamentally misestimate agent-facing web adoption due to dual distortion: widespread HTML soft-404s masquerading as HTTP 200 responses in crawl indices (accounting for over half of archived responses in high-traffic strata), compounded by crawler frontier bias that severely under-represents tail adopters. To resolve these measurement errors, we develop and validate a multi-signal classification gate combining DOM structure, content-length heuristics, homepage similarity metrics, and MIME verification, achieving high inter-annotator agreement (Cohen's kappa > 0.80) against human validation ground truth. We further analyse the structural payload characteristics of genuine agent files, revealing heavy reliance on automated platform generators and widespread broken links. Our findings provide a rigorous measurement methodology, open-source pipeline, and reference dataset for studying agent-facing web protocol evolution.

---

## Author & Anonymous Statement

This manuscript is submitted under the double-blind review policy of ACM IMC'27. In compliance with conference guidelines:
1. All author names, institutional affiliations, and direct acknowledgments have been omitted from the manuscript and supplementary files.
2. Anonymised replication packages and validation scripts are provided for artifact review.
3. The study addresses core internet measurement questions regarding crawl index fidelity, HTTP status semantics, and protocol deployment characterisation.

---

## Sequential Fallback & Ethics Declaration

This submission package represents **Plan C** for Demo 20 (`agent-web-census`):
- It remains strictly **dormant** and will only be activated if prior options (Plan A: WWW'27 Research Track, and Plan B: WWW'27 Short Paper) have received formal rejection decisions.
- Ethical considerations adhere strictly to the Menlo Report: all crawl data is secondary from public Common Crawl releases; live active probes are rate-limited, strictly bounded, and non-intrusive.
- The work is original and will not be under simultaneous review at any other venue upon activation.
