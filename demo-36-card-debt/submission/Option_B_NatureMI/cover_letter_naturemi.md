# Author Cover Letter — Nature Machine Intelligence

**To**: The Editors, *Nature Machine Intelligence*  
**Journal**: Nature Machine Intelligence (Springer Nature)  
**Submission Category**: Article / Analysis  
**Submission Mode**: Rolling Submission (Plan B Fallback)

---

## Submission Overview

- **Title**: The download-weighted safety gap on public machine learning model registries is falsified on registered estimators
- **Author**: Dr Petar Radanliev (The Open University, University of Oxford)
- **Corresponding Author**: `petar.radanliev@open.ac.uk`
- **Keywords**: machine learning governance, open-weight models, model cards, safety disclosure, extreme value theory, algorithmic accountability

---

## Editorial Rationale & Significance

We submit for your consideration our empirical investigation into the safety disclosure and documentation debt of public machine learning model registries.

Open-weight machine learning checkpoints hosted on public repositories (such as the Hugging Face Hub) increasingly constitute critical digital infrastructure across modern computing. While corporate and policy stakeholders frequently assume that market popularity acts as an informal quality filter—where models downloaded millions of times carry more rigorous safety documentation than obscure experimental uploads—our study tests this assumption across an exhaustive repository census of 809,703 model cards and 48,247 supply-chain lineage edges accounting for 2.47 billion downloads.

Our findings reveal two critical insights for the machine learning community:
1. **Falsification of the Popularity Dividend**: On a pre-registered binned estimator, the popularity gap is $-2.9$ percentage points and therefore falsified. Even on an unregistered row-level vector, the apparent gap (+11.21 points) is statistically indeterminate under bootstrap resampling (95% CI: [$-1.67$, $+24.68$] points).
2. **Infinite-Variance Pareto Dynamics**: Extreme Value Theory establishes that model consumption operates in an infinite-variance regime ($\alpha = 0.98 \le 2$). A single high-traffic model swings the global safety metric by 7.20 percentage points, and trimming just the top ten models reduces the popularity gap to $+1.34$ points. Furthermore, derivative lineages suffer severe documentation decay, with an 83.46% license omission rate on model merges.

These results have immediate relevance for regulatory compliance under the EU AI Act and national AI safety institutes, demonstrating that unadjusted download weighting creates brittle and misleading indicators of open model risk.

---

## Sequential Submission Status

This manuscript is prepared as **Plan B** in the project's dissemination portfolio. It is currently dormant while Plan A is under evaluation at The Web Conference 2027 (WWW'27). In strict adherence to Springer Nature and international publishing ethics, this submission will only be activated following an explicit, final rejection decision from WWW'27. No simultaneous or concurrent submission is undertaken.
