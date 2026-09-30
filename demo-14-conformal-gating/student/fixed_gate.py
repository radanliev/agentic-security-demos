#!/usr/bin/env python3
"""Fixed-threshold baseline for Demo 14.

Same interface as the conformal gate but with a hard-coded threshold,
showing what a heuristic gate without calibration would do.
"""


class FixedGate:
    """Baseline gate that always uses threshold 0.50."""

    def __init__(self, threshold: float = 0.50) -> None:
        self.threshold = threshold

    def decide(self, score: float) -> bool:
        """Return True (execute) when score is at or below threshold."""
        return score <= self.threshold
