#!/usr/bin/env python3
"""Agent-facing web census helpers for Demo 20.

Adoption means a site publishes agent directives (either flag).
Exposure means its synthetic copy carries injection text.
"""


def adopted(site: dict) -> bool:
    """Return True when the site publishes agent directives."""
    return bool(site.get("llms_txt") or site.get("ai_directive"))


def exposed(site: dict) -> bool:
    """Return True when the site carries injection text."""
    return bool(site.get("injection_text"))
