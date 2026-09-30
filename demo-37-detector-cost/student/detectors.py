#!/usr/bin/env python3
"""Two toy prompt-injection detectors for Demo 37.

Both are plain substring rules over synthetic fixture text. They measure
nothing about real detectors; they exist so students can compare operating
points under asymmetric error costs.
"""

STRICT_MARKER = "ignor"
LENIENT_PHRASE = "ignore previous instructions"


def strict(text: str) -> bool:
    """Flag any text containing the substring 'ignor' (case-insensitive)."""
    return STRICT_MARKER in text.lower()


def lenient(text: str) -> bool:
    """Flag only texts carrying the exact phrase 'ignore previous instructions'."""
    return LENIENT_PHRASE in text.lower()
