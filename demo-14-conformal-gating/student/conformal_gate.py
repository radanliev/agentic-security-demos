#!/usr/bin/env python3
"""Conformal-style gate for Demo 14.

The gate never sees labels. It only decides: execute an action when its
risk score is at or below a calibrated threshold. Calibration (choosing the
threshold) lives in the evaluator, which may read the answer key.
"""


class ConformalGate:
    """Threshold gate with a calibrated risk budget."""

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def decide(self, score: float) -> bool:
        """Return True (execute) when score is at or below threshold."""
        return score <= self.threshold
