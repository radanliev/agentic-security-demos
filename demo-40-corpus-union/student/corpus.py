#!/usr/bin/env python3
"""Corpus union helpers for Demo 40.

Normalises record texts (lowercase + strip), dedupes by SHA-256, then
applies a licence gate that admits only permissive and by-sa records.
All inputs are synthetic teaching records.
"""

import hashlib

ALLOWED = ("permissive", "by-sa")


def normalize(text: str) -> str:
    """Lowercase and strip surrounding whitespace."""
    return text.lower().strip()


def digest(text: str) -> str:
    """SHA-256 hex digest of the normalised text."""
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def dedupe(records: list) -> list:
    """Keep the first record per normalised-text digest."""
    seen: dict = {}
    for rec in records:
        seen.setdefault(digest(rec["text"]), rec)
    return list(seen.values())


def releasable(records: list) -> list:
    """Keep deduped records whose licence is permissive or by-sa."""
    return [r for r in dedupe(records) if r["license"] in ALLOWED]
