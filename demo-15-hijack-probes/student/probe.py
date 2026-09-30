#!/usr/bin/env python3
"""White-box hijack probe for Demo 15.

The probe never sees labels. It flags an episode as hijacked when its
probe score meets or exceeds a fixed threshold.
"""


class Probe:
    """Threshold probe over scalar probe scores."""

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def decide(self, score: float) -> bool:
        """Return True (flag hijacked) when score >= threshold."""
        return score >= self.threshold
