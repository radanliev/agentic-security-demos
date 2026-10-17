# Author Cover Letter — ICSE 2028 (Research Track)

**To**: Program Committee Co-Chairs  
**Conference**: 50th IEEE/ACM International Conference on Software Engineering (ICSE 2028)  
**Track**: Research Track  
**Submission Portal**: HotCRP / ConfTool (per conference CFP)  

---

## Submission Details

- **Title**: What a Client Fetches: Default-Path Exposure of Models in Software Supply Chains
- **Track**: Research Track
- **Keywords**: Software supply chain, machine learning engineering, model registries, default-path exposure, serialisation security, licence compliance
- **Submission Type**: Full Technical Paper (10 pages plus 2 pages of references)

---

## Abstract

Software engineering increasingly relies on pre-trained machine learning models downloaded from public hubs as external components. In traditional package ecosystems like npm or PyPI, dependency managers resolve immutable packages. In contrast, model hubs rely on self-reported lineage metadata, where fine-tunes duplicate and modify weights. We examine whether derived models inherit software execution risks and licence incompatibilities from parent models. We introduce a distinction between file presence and default-path exposure: whether automated loaders execute hazardous files under default settings. In a comprehensive census of 48,247 fine-tune lineage edges spanning 16 foundational base models on Hugging Face, 0 of 16 base models exhibit default-path serialisation exposure. Across derived models, 3.17% exhibit default-path serialisation exposure, while 54.90% contain legacy pickle files safely ignored by modern loaders. Downstream developers introduce pickle files into safe lineages 8.5x more often than they repair them. Furthermore, 11.22% of models declaring licences introduce incompatible terms, and 44.21% drop licences entirely. These empirical findings demonstrate that model supply-chain defects stem predominantly from unvetted downstream repository mutations rather than inheritance from upstream foundations, providing actionable guidelines for software engineering dependency verification.

---

## Software Engineering Contributions

This paper addresses critical challenges at the intersection of empirical software engineering, software supply chain security, and machine learning components:
1. **Dependency & Provenance Analysis**: Empirical characterisation of a novel component distribution ecosystem (model registries) distinct from traditional package registries.
2. **Defect Inheritance vs Downstream Mutation**: Quantifying that software hazards (unsafe serialisation formats, remote execution scripts, licence drift) originate predominantly from downstream maintainer practices (8.5:1 introduction-to-repair ratio) rather than upstream foundations.
3. **Actionable Verification Gates**: Practical principles for implementing fail-closed dependency resolution and AIBOM checks in software development workflows.

---

## Author & Double-Blind Statement

This manuscript adheres strictly to ICSE 2028 double-blind review requirements:
1. All author identities, affiliations, and funding disclosures have been omitted.
2. Self-references are written in the third person.
3. Replication scripts, datasets, and package trees are provided through an anonymised repository.

---

## Sequential Submission Policy Statement

The authors confirm that this manuscript represents original, unpublished research. This package serves as a **sequential Plan B fallback** and will only be activated if the manuscript is formally rejected by The Web Conference 2027 (WWW'27), where decisions are expected in January 2027. Under no circumstances will concurrent or overlapping submission occur.
