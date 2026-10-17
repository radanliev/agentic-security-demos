# Author Cover Letter — Patterns (Cell Press)

**To**: The Editors, *Patterns*  
**Journal**: Patterns (Cell Press)  
**Article Type**: Research Article / Data Science in Practice  
**Submission Mode**: Rolling Submission (Plan C Fallback)

---

## Submission Details

- **Title**: Fragility of Download-Weighted Safety Metrics on Public Model Registries: An Empirical Census and Heavy-Tail Analysis
- **Author**: Dr Petar Radanliev (The Open University, The Alan Turing Institute, University of Oxford)
- **Corresponding Author**: `petar.radanliev@open.ac.uk`
- **Keywords**: data stewardship, model cards, open science, extreme value theory, machine learning governance, data infrastructure

---

## Editorial Significance for Patterns

We submit for your consideration our data-science investigation into documentation debt and heavy-tailed exposure metrics across public machine learning registries.

Public model repositories represent foundational data infrastructure for modern artificial intelligence. However, assessing the societal risk and documentation quality of distributed models relies heavily on usage metrics such as cumulative download counts. Our study executes an exhaustive empirical audit of 809,703 model cards and 48,247 supply-chain lineage edges on the Hugging Face Hub (accounting for 2.47 billion downloads).

Our findings provide fundamental methodological and data stewardship contributions:
1. **Falsification of Popularity-Driven Quality**: On a pre-registered binned estimator, the hypothesis that high-download models maintain superior safety documentation is falsified ($-2.9$ percentage points).
2. **Infinite-Variance Heavy Tails in Data Registries**: Applying Extreme Value Theory (EVT), we demonstrate that public model downloads follow a Pareto power law with tail index $\alpha = 0.98 \le 2$. This establishes that public model consumption operates in an infinite-variance regime where naive download weighting breaks down. The global weighted safety disclosure rate is hyper-sensitive to individual corporate models: omitting the single most popular model alone swings the global metric by 7.20 percentage points.
3. **Data Provenance & Licensing Decay**: Tracing supply-chain dependencies reveals that downstream model merges fail to carry upstream licenses in 83.46% of cases, creating unmonitored documentation debt.

These findings directly inform data stewards, registry curators, and policy analysts, establishing that unadjusted download weighting is unsuitable for trustworthy AI governance and highlighting the necessity of tail-trimmed indicators.

---

## Sequential Dissemination Statement

This package represents **Plan C** in our sequential publication protocol. It is currently dormant and will only be activated if formal rejections are received from both Plan A (The Web Conference 2027) and Plan B (Nature Machine Intelligence). No concurrent or simultaneous submission is undertaken.
