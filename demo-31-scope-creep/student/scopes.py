#!/usr/bin/env python3
"""Scope helpers for Demo 31.

An integration is over-privileged when its requested scopes strictly
superset its used scopes. The least-privilege set is the sorted union
of every scope actually used.
"""


def overprivileged(integration: dict) -> bool:
    """Return True when requested scopes strictly exceed used scopes."""
    requested = set(integration.get("requested", []))
    used = set(integration.get("used", []))
    return requested > used


def least_privilege(integrations: list) -> list:
    """Return the sorted union of all used scopes."""
    union = set()
    for integration in integrations:
        union.update(integration.get("used", []))
    return sorted(union)


def check_all(integrations: list) -> dict:
    """Partition integrations into over-privileged and tight ids."""
    over = [i["id"] for i in integrations if overprivileged(i)]
    tight = [i["id"] for i in integrations if not overprivileged(i)]
    return {"over": sorted(over), "tight": sorted(tight)}
