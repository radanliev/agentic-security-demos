"""Offline equity audit of input guardrails across writing variants (demo 51)."""
from .core import REFERENCE, disparity, fit_thresholds, flagged, paired_flip_rate, rates

__all__ = ["REFERENCE", "disparity", "fit_thresholds", "flagged", "paired_flip_rate", "rates"]
__version__ = "0.1.0"
