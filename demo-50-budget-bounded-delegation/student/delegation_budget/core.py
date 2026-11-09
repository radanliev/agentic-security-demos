"""Budget-attenuated delegation for multi-agent pipelines (defensive, offline).

A token budget is carried down a delegation tree as an attenuating capability:
a child can only receive part of what its parent still holds, so no chain of
delegation can spend more than its root principal's budget. A request that would
break an invariant is denied (fail-closed). The plans in ``fixtures/`` are
synthetic placeholders that exercise the code; they are not measurements.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

INVARIANTS = {
    "B1": "a node's own spend plus what it has delegated never exceeds its grant",
    "B2": "delegation depth never exceeds the configured maximum",
    "B3": "no node delegates to more children than the configured fan-out cap",
    "B4": "every child's grant was within its parent's remaining budget when it was made",
    "B5": "total spend across the tree never exceeds the root budget",
}


@dataclass
class Node:
    node_id: str
    parent: str | None
    depth: int
    granted: int
    spent: int = 0
    delegated: int = 0
    children: list = field(default_factory=list)

    @property
    def remaining(self) -> int:
        return self.granted - self.spent - self.delegated


@dataclass(frozen=True)
class Decision:
    op: str
    node: str
    requested: int
    granted: int
    allowed: bool
    reason: str


class BudgetLedger:
    """Enforces invariants B1 to B5 on a delegation tree rooted at one principal."""

    def __init__(
        self,
        root_id: str,
        root_budget: int,
        max_depth: int,
        max_fanout: int,
        allow_partial: bool = False,
    ) -> None:
        if root_budget < 0 or max_depth < 0 or max_fanout < 0:
            raise ValueError("budget, depth and fan-out limits must be non-negative")
        self.root_id = root_id
        self.root_budget = root_budget
        self.max_depth = max_depth
        self.max_fanout = max_fanout
        self.allow_partial = allow_partial
        self.nodes: dict[str, Node] = {root_id: Node(root_id, None, 0, root_budget)}
        self.grant_snapshots: dict[str, int] = {}
        self.log: list[Decision] = []

    def _record(self, decision: Decision) -> Decision:
        self.log.append(decision)
        return decision

    def delegate(self, parent_id: str, child_id: str, requested: int) -> Decision:
        parent = self.nodes.get(parent_id)
        if parent is None:
            return self._record(Decision("delegate", child_id, requested, 0, False, "unknown parent"))
        if child_id in self.nodes:
            return self._record(Decision("delegate", child_id, requested, 0, False, "node already exists"))
        if requested <= 0:
            return self._record(Decision("delegate", child_id, requested, 0, False, "request must be positive"))
        if parent.depth + 1 > self.max_depth:
            return self._record(Decision("delegate", child_id, requested, 0, False, "depth cap"))
        if len(parent.children) >= self.max_fanout:
            return self._record(Decision("delegate", child_id, requested, 0, False, "fan-out cap"))
        available = parent.remaining
        if requested > available and not self.allow_partial:
            return self._record(
                Decision("delegate", child_id, requested, 0, False, "exceeds parent's remaining budget")
            )
        grant = min(requested, available)
        if grant <= 0:
            return self._record(Decision("delegate", child_id, requested, 0, False, "parent budget exhausted"))
        self.grant_snapshots[child_id] = available
        self.nodes[child_id] = Node(child_id, parent_id, parent.depth + 1, grant)
        parent.delegated += grant
        parent.children.append(child_id)
        reason = "granted" if grant == requested else "granted in part"
        return self._record(Decision("delegate", child_id, requested, grant, True, reason))

    def spend(self, node_id: str, amount: int) -> Decision:
        node = self.nodes.get(node_id)
        if node is None:
            return self._record(Decision("spend", node_id, amount, 0, False, "unknown node"))
        if amount <= 0:
            return self._record(Decision("spend", node_id, amount, 0, False, "amount must be positive"))
        if amount > node.remaining:
            return self._record(Decision("spend", node_id, amount, 0, False, "exceeds remaining budget"))
        node.spent += amount
        return self._record(Decision("spend", node_id, amount, amount, True, "spent"))

    def total_spent(self) -> int:
        return sum(n.spent for n in self.nodes.values())

    def denials(self) -> list[Decision]:
        return [d for d in self.log if not d.allowed]

    def audit(self) -> dict[str, bool]:
        nodes = list(self.nodes.values())
        return {
            "B1": all(n.spent + n.delegated <= n.granted for n in nodes),
            "B2": all(n.depth <= self.max_depth for n in nodes),
            "B3": all(len(n.children) <= self.max_fanout for n in nodes),
            "B4": all(self.nodes[c].granted <= snap for c, snap in self.grant_snapshots.items()),
            "B5": self.total_spent() <= self.root_budget,
        }


def replay(plan: Mapping) -> BudgetLedger:
    """Replay a plan of delegate and spend events through a fresh ledger."""
    ledger = BudgetLedger(
        plan["root"],
        plan["root_budget"],
        plan["max_depth"],
        plan["max_fanout"],
        plan.get("allow_partial", False),
    )
    for event in plan["events"]:
        op = event["op"]
        if op == "delegate":
            ledger.delegate(event["parent"], event["child"], event["tokens"])
        elif op == "spend":
            ledger.spend(event["node"], event["tokens"])
        else:
            raise ValueError(f"unknown op {op!r}")
    return ledger


def requested_spend(plan: Mapping) -> int:
    """Total spend the plan asks for if every request were honoured without a ledger."""
    return sum(e["tokens"] for e in plan["events"] if e["op"] == "spend")
