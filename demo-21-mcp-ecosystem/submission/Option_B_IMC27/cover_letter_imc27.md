# Author Cover Letter — ACM Internet Measurement Conference 2027 (IMC'27)

**To**: Program Committee Co-Chairs  
**Conference**: ACM Internet Measurement Conference 2027 (IMC'27)  
**Track**: Research Track — Internet Measurement and Web Protocols  
**Submission Portal**: HotCRP / OpenReview (IMC'27 Portal)

---

## Submission Details

- **Title**: Measuring the Model Context Protocol: Remote Endpoints, Secret Headers, and Domain Migrations in the Agentic Web
- **Track**: Research Track — Internet Measurement and Web Protocols
- **Keywords**: Internet measurement, Model Context Protocol, agentic systems, HTTP endpoints, domain migrations, Web infrastructure
- **Submission Type**: Full Research Paper (ACM SIGCONF / IMC format)

---

## Abstract

The Model Context Protocol (MCP) establishes a standardised web application interface connecting autonomous language model agents to remote microservices. We perform a comprehensive, longitudinal measurement of the official MCP registry across 126,847 version records and 37,815 distinct servers. Our network measurement reveals that 61.89% of registered servers declare remote HTTP endpoints and 56.96% operate purely as remote web services without installable packages. These endpoints resolve to 15,738 distinct hosts across 6,432 registrable domains, with 79.5% unranked in the Tranco Top-1M. Furthermore, 3,679 endpoints demand confidential headers marked isSecret, binding ambient credentials to outbound web requests. Across 89,032 publication-ordered version transitions, releases arrive rapidly (median interval 0.8 days, 52.4% within 24 hours). Longitudinal tracking reveals 1,353 transitions modifying remote URLs, with 52.4% changing destination hostnames and 36.1% crossing administrative eTLD+1 boundaries, predominantly migrating to multi-tenant serverless or PaaS platforms. Syntactic pattern screening across 40,672 tool descriptions yields a 1.25% flag rate, but recovers only 6.2% of benchmark prompt injection attacks while flagging benign documentation in 89.2% of real-world hits. We present architectural recommendations for origin-bound credential scoping, out-of-band manifest attestations, and registry domain lifecycle verification to secure agentic web infrastructure.

---

## Author & Anonymous Statement

This manuscript is submitted under the mandatory double-blind review policy of IMC'27. In compliance with the conference guidelines:
1. All author identities, institutional affiliations, and acknowledgments have been strictly omitted.
2. Anonymised data artifacts and reproduction scripts are referenced without identifiable commit or repository histories.
3. The empirical study focuses on network measurement, endpoint properties, and infrastructure transitions in the emerging agentic Web.

---

## Sequential Policy & Fallback Declaration

**Status**: `pending` (Sequential Plan B fallback).

This submission package represents Plan B in our publication roadmap. It remains **strictly dormant** while Plan A is under evaluation at The Web Conference 2027 (WWW'27). It will only be activated if an explicit rejection decision is rendered by WWW'27 (notification scheduled for 04 January 2027). Under no circumstances will this work be submitted concurrently or in violation of dual-submission rules.
