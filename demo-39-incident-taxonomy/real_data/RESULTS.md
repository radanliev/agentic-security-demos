# Results: AVID reports tallied against the Demo 39 patterns

Command: `python3 analyse.py /tmp/avid`. Output: `results.json`.

- 1,745 reports. The year folders are very uneven (2022: 5, 2023: 3, 2025: 25, 2026: 1,712), which suggests a bulk import in 2026. This needs checking before any trend claim is made.
- Risk domain: Security 1,470, Performance 87, Ethics 56.
- Most frequent SEP view codes: S0100 (software vulnerability) 1,111, S0403 283, S0301 112.
- Keyword screen for the four toy patterns (multi-label): tool-misuse 518, data-exfiltration 154, prompt-injection 140, privilege-escalation 122; 924 match none.

Reading. On real records the toy's ordering does not hold. In this corpus, prompt injection is not the most common pattern, and more than half the reports fall outside all four patterns. That is the empirical point a practitioner taxonomy has to handle. The screen is a regex over description text, so "tool" over-matches, and its counts are only a triage signal. A FAccT or S&P Magazine paper would need a coded sample with a stated codebook, and might add the AI Incident Database (https://incidentdatabase.ai), which is not yet ingested.
