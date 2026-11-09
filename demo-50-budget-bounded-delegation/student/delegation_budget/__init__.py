"""Offline budget-attenuated delegation ledger for multi-agent pipelines (demo 50)."""
from .core import INVARIANTS, BudgetLedger, Decision, Node, replay, requested_spend

__all__ = ["INVARIANTS", "BudgetLedger", "Decision", "Node", "replay", "requested_spend"]
__version__ = "0.1.0"
