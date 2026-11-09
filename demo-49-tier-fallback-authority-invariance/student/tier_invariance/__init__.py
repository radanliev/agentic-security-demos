"""Offline checks of authority invariance across model-tier transitions (demo 49)."""
from .core import (
    RULES,
    TIERS,
    ReferenceMonitor,
    Violation,
    check_trace,
    expected_decision,
    summarise,
)

__all__ = [
    "RULES",
    "TIERS",
    "ReferenceMonitor",
    "Violation",
    "check_trace",
    "expected_decision",
    "summarise",
]
__version__ = "0.1.0"
