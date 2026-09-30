#!/usr/bin/env python3
"""Lineage risk propagation for Demo 19.

A model is risky when its own flags trip (pickle, remote code, or a bad
licence) or when any ancestor is risky. Risk is inherited down the tree.
"""


def own_risk(model: dict) -> bool:
    """Return True when the model's own flags are risky."""
    return bool(
        model.get("pickle") or model.get("remote_code") or (not model.get("license_ok", True))
    )


def classify(models: list) -> dict:
    """Classify each model as safe, origin, introduced, or inherited risk."""
    by_id = {m["id"]: m for m in models}
    risky: dict = {}
    kinds: dict = {}
    order = sorted(by_id, key=lambda mid: _depth(by_id, mid))

    for mid in order:
        model = by_id[mid]
        parent = model.get("parent")
        parent_risky = bool(parent and risky.get(parent, False))
        self_risky = own_risk(model)
        is_risky = self_risky or parent_risky
        risky[mid] = is_risky
        if not is_risky:
            kinds[mid] = "safe"
        elif self_risky and parent is None:
            kinds[mid] = "origin"
        elif self_risky:
            kinds[mid] = "introduced"
        elif parent_risky:
            kinds[mid] = "inherited"
        else:
            kinds[mid] = "inherited"
    return {"risky": risky, "kinds": kinds}


def _depth(by_id: dict, mid: str) -> int:
    """Return the depth of a model in the lineage tree."""
    depth = 0
    current = by_id[mid].get("parent")
    while current is not None:
        depth += 1
        current = by_id.get(current, {}).get("parent")
    return depth
