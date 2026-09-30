#!/usr/bin/env python3
"""MemScope auditor for Demo 28.

Flags memory entries containing literal instruction patterns
(case-insensitive substring match). A teaching stand-in for a
memory-integrity audit tool.
"""

PATTERNS = (
    "remember to exfiltrate",
    "always send credentials to",
    "ignore previous instructions",
)


def audit(entries: list) -> list:
    """Return ids of entries containing any poison pattern."""
    flagged = []
    for e in entries:
        text = e.get("text", "").lower()
        if any(p in text for p in PATTERNS):
            flagged.append(e["id"])
    return flagged
