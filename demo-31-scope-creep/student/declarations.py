#!/usr/bin/env python3
"""Declaration helpers for Demo 31.

An integration has a declaration gap when its declared authority strictly
supersedes its exercised authority. The least-declaration set is the sorted
union of every authority actually exercised.
"""


def gapped(integration: dict) -> bool:
    """Return True when declared authority strictly exceeds exercised authority."""
    declared = set(integration.get("declared", []))
    exercised = set(integration.get("exercised", []))
    return declared > exercised


def least_declaration(integrations: list) -> list:
    """Return the sorted union of all exercised authority."""
    union = set()
    for integration in integrations:
        union.update(integration.get("exercised", []))
    return sorted(union)


def check_all(integrations: list) -> dict:
    """Partition integrations into gapped and tight ids."""
    over = [i["id"] for i in integrations if gapped(i)]
    tight = [i["id"] for i in integrations if not gapped(i)]
    return {"over": sorted(over), "tight": sorted(tight)}
