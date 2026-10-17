# Author Cover Letter — FSE 2028 (Research Track)

**To**: Program Committee Co-Chairs  
**Conference**: ACM International Conference on the Foundations of Software Engineering (FSE 2028)  
**Track**: Research Track  
**Submission Portal**: HotCRP / ConfTool  

---

## Submission Details

- **Title**: What a Client Fetches: Default-Path Exposure of Models in Software Supply Chains
- **Track**: Research Track
- **Keywords**: Software supply chain, empirical software engineering, model registries, default-path exposure, serialisation security, licence compliance
- **Submission Type**: Full Research Paper (ACM SIGCONF format, 10 pages plus references)

---

## Abstract

Modern software systems increasingly integrate foundation models distributed through Web registries. Understanding the foundations of model supply chains requires rigorous analysis of how software risks propagate across derivation graphs. This empirical study investigates model lineage across 48,247 parent-child derivation edges rooted in 16 base models on Hugging Face. We formalise the distinction between static file presence and default-path execution exposure in automated model loading. Our census reveals that 0 of 16 base models exhibit default-path serialisation exposure; inheritance of default-path deserialisation risk is not identified. Across downstream models, 3.17% exhibit default-path serialisation exposure, whereas 54.90% maintain presence without exposure. Downstream mutations introduce hazardous serialisation into previously safe lineages at an introduction-to-repair ratio of 8.5:1. Additionally, 11.22% of declared children launder upstream licences, and 44.21% omit licensing entirely. These results show that empirical software engineering risks in model hubs originate predominantly through downstream mutation rather than architectural inheritance. We propose rigorous foundations for model dependency management, verification gates, and supply-chain assurance.

---

## Foundational Contributions

1. **Formal Separation of Presence vs Exposure**: Mathematical and algorithmic formalisation of default-path resolution in dynamic model registries.
2. **Empirical Lineage Verification**: Complete census of 48,247 derivation edges evaluating risk transmission, demonstrating that risk is introduced by downstream mutation rather than parent inheritance.
3. **Software Architecture & Assurance Foundations**: Principled foundations for verifying model dependencies in modern software systems.

---

## Author & Double-Blind Statement

This manuscript complies with FSE 2028 double-blind review standards:
1. All author names, institutional affiliations, and acknowledgments are strictly omitted.
2. Self-citations are written in the third person.
3. Replication scripts, census tools, and test suites are provided via an anonymised release.

---

## Sequential Submission Policy Statement

The authors confirm that this work is original and unpublished. This package serves as a **sequential Plan C fallback** and remains strictly dormant unless and until explicit rejection decisions have been received from both WWW'27 (Plan A) and ICSE'28 (Plan B). No concurrent submission will occur.
