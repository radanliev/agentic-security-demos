# Author Cover Letter — The Web Conference 2027 (WWW'27)

**To**: Program Committee Co-Chairs and Track Chairs  
**Conference**: The Web Conference 2027 (WWW'27), Dublin, Ireland (10–14 May 2027)  
**Track**: Research Track — Responsible Web  
**Submission Portal**: OpenReview (`https://openreview.net/group?id=ACM.org/TheWebConf/2027`)

---

## Submission Details

- **Title**: The Download-Weighted Safety Gap on a Public Model Registry Is Falsified on the Registered Estimator
- **Track**: Research Track — Responsible Web
- **Keywords**: Responsible Web, Algorithmic Accountability, Model Cards, Safety Disclosure, Web Registries, Download Weighting
- **Submission Type**: Full Research Paper (ACM SIGCONF format, 8 pages main text, up to 12 pages total)

---

## Abstract

Model cards serve as the primary accountability documents published with open-weight models on public Web registries. A central question for the Responsible Web is whether models that circulate widely and power downstream Web applications carry higher standards of safety documentation than the background repository population. This study investigates safety disclosure across 809,703 model cards and 48,247 supply-chain derivation edges on the Hugging Face Hub, accounting for 2.47 x 10^9 cumulative downloads. Evaluating a retrospectively registered popularity hypothesis (confirmed iff the gap reaches +15 points; falsified below +10 points), the registered binned estimator yields -2.9 points and is therefore falsified. The unregistered row-level estimate places the download-weighted rate at 38.40% against 27.19% unweighted (gap +11.21 points), with a bootstrap (1,000 resamples) 95% interval of [-1.67, +24.68] points that covers both boundaries and is indeterminate. Hill estimates from Extreme Value Theory (EVT) indicate that public model downloads are consistent with an infinite-variance Pareto regime (Hill tail index alpha = 0.98 <= 2), where classical Central Limit convergence breaks down. The weighted safety rate is driven by extreme leverage from a handful of corporate models: omitting the single most popular model alone swings the global weighted safety rate by 7.20 percentage points, and trimming the top ten models compresses the popularity gap to just +1.34 percentage points. Furthermore, lineage analysis across derivative models reveals severe documentation decay, with an 83.46% licence omission rate among model merges. These findings indicate that unadjusted download weighting yields statistically brittle accountability metrics on the Web, highlighting the necessity of tail-trimmed indicators and supply-chain provenance tracking for responsible Web AI governance.

---

## Author & Anonymous Statement

This manuscript is submitted under the mandatory double-blind review policy of The Web Conference 2027. In compliance with the conference guidelines:
1. All author names, institutional affiliations, and direct identifying references have been omitted from the manuscript and supplementary materials.
2. Any referenced analysis scripts, macro generators, and experimental outputs are provided via anonymised repositories without identifying git commit metadata or local author paths.
3. The research questions explicitly investigate a central challenge for the Responsible Web: the empirical transparency, safety disclosure, and documentation debt of open-weight models distributed across public Web registries and embedded into client-side and server-side Web systems.

---

## OpenReview Intent & Author Cap Compliance

The author declares the formal intent to register this submission on the official OpenReview portal prior to the abstract registration deadline of **18 October 2026 23:59 AoE**, followed by final PDF manuscript upload before **25 October 2026 23:59 AoE**.

Furthermore, the author complies with the WWW'27 author cap policy (no author exceeds the maximum limit of seven research-track submissions across the conference).

---

## Dual Submission Declaration

This manuscript presents original, unpublished work. It has not been published elsewhere, nor is it concurrently submitted or under active consideration at any other conference, journal, or workshop. Post-rejection sequential fallbacks (Plan B: Nature Machine Intelligence; Plan C: Patterns) will only be activated in the event of an explicit rejection decision from WWW'27.
