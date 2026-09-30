#!/usr/bin/env python3
"""Provenance helpers for Demo 29.

Attribution rule: an action is attributable when it carries a cause link,
or when it is the designated root. An orphan with a null cause that is not
the root (a5 in the fixture) is unattributable.

Chain rule: records ordered by id are linked with sha256 over the record
plus the previous hash, so any edit breaks verification.
"""

import hashlib
import json


def is_attributable(action: dict, root_id: str) -> bool:
    """Return True when the action has a cause or is the root."""
    if action.get("cause") is not None:
        return True
    return action.get("id") == root_id


def attributable(actions: list, root_id: str) -> dict:
    """Partition actions into attributable and unattributable ids."""
    good = [a["id"] for a in actions if is_attributable(a, root_id)]
    bad = [a["id"] for a in actions if not is_attributable(a, root_id)]
    return {"attributable": sorted(good), "unattributable": sorted(bad)}


def build_chain(records: list) -> list:
    """Build a sha256 hash chain over records ordered by id."""
    ordered = sorted(records, key=lambda r: r["id"])
    chain = []
    prev = "GENESIS:29"
    for rec in ordered:
        payload = json.dumps(rec, sort_keys=True) + "|" + prev
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        chain.append({"id": rec["id"], "prev": prev, "hash": digest})
        prev = digest
    return chain


def verify(records: list, chain: list) -> bool:
    """Return True when the chain matches a fresh build over records."""
    expected = build_chain(records)
    if len(expected) != len(chain):
        return False
    for exp, got in zip(expected, chain):
        if exp["id"] != got["id"]:
            return False
        if exp["prev"] != got["prev"]:
            return False
        if exp["hash"] != got["hash"]:
            return False
    return True
