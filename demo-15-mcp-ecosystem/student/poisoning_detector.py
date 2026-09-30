#!/usr/bin/env python3
"""Poisoning detector for Demo 15.

Flags a server description when it contains a model-directed instruction
pattern. Patterns are literal substrings only — no network, no models.
"""

PATTERNS = (
    "ignore previous instructions",
    "exfiltrate",
    "send credentials to",
)


def is_poisoned(description: str) -> bool:
    """Return True when the description contains a poisoning pattern."""
    lowered = description.lower()
    return any(p in lowered for p in PATTERNS)
