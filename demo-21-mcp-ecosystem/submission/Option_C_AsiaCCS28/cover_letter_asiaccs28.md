# Author Cover Letter — ACM ASIA Conference on Computer and Communications Security 2028 (AsiaCCS'28)

**To**: Program Committee Co-Chairs  
**Conference**: ACM ASIA Conference on Computer and Communications Security 2028 (AsiaCCS'28)  
**Track**: Software & Systems Security / AI & Agent Security  
**Submission Portal**: HotCRP / OpenReview (AsiaCCS'28 Portal)

---

## Submission Details

- **Title**: Security Boundaries of Agentic Tool Registries: Empirical Analysis of Remote Endpoints, Credentials, and Version Drift in MCP
- **Track**: Software & Systems Security / AI & Agent Security
- **Keywords**: AI security, Model Context Protocol, agentic systems, tool poisoning, HTTP endpoints, provenance attestations
- **Submission Type**: Full Research Paper (ACM SIGCONF format, 12 pages)

---

## Abstract

The Model Context Protocol (MCP) establishes a standardised web application interface connecting autonomous language model agents to external tools and microservices. We present an empirical security measurement of the official MCP registry across 126,847 version records and 37,815 distinct servers. Our study reveals significant attack surfaces: 61.89% of registered servers declare remote HTTP endpoints, 56.96% operate purely as remote web services without installable packages, and 3,679 endpoints demand confidential headers marked isSecret, binding ambient credentials to outbound web requests. Across 89,032 publication-ordered version transitions, releases arrive rapidly (median interval 0.8 days, 52.4% within 24 hours). Longitudinal tracking reveals 1,353 transitions modifying remote URLs, with 52.4% altering destination hostnames and 36.1% crossing administrative eTLD+1 boundaries, predominantly migrating to multi-tenant serverless or PaaS platforms. Syntactic pattern screening across 40,672 tool descriptions yields a 1.25% flag rate, but recovers only 6.2% of benchmark prompt injection attacks while flagging benign documentation in 89.2% of real-world hits, proving syntactic filters insufficient as security boundaries. We propose three architectural defences---origin-bound credential scoping, out-of-band manifest attestations, and registry domain lifecycle verification---to secure agentic tool execution.

---

## Author & Anonymous Statement

This manuscript is submitted under the mandatory double-blind review policy of AsiaCCS'28. In compliance with the conference guidelines:
1. All author identities, institutional affiliations, and acknowledgments have been strictly omitted.
2. Anonymised data artifacts and reproduction scripts are referenced without identifiable commit or repository histories.
3. The empirical study focuses on software security, threat modeling, and defensive mechanisms in autonomous agent tool protocols.

---

## Sequential Policy & Fallback Declaration

**Status**: `pending` (Sequential Plan C fallback).

This submission package represents Plan C in our publication roadmap. It remains **strictly dormant** while Plan A is under evaluation at The Web Conference 2027 (WWW'27) and Plan B is under consideration at IMC'27. It will only be activated if explicit rejection decisions are rendered sequentially by both WWW'27 and IMC'27. Under no circumstances will this work be submitted concurrently or in violation of dual-submission rules.
