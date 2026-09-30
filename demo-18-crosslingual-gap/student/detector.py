#!/usr/bin/env python3
"""English-centric injection detector for Demo 18.

Flags a text only when it contains the English phrase or the marker.
It has no multilingual logic, which is the point of the lesson.
"""


def flagged(text: str) -> bool:
    """Return True when the text trips the detector."""
    return ("ignore previous instructions" in text) or ("[TOOL]" in text)
