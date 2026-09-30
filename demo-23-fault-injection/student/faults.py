#!/usr/bin/env python3
"""Fault-outcome table for Demo 23.

Deterministic mapping from fault type to pipeline outcome, with and
without a retry budget. Without retries most faults escape gracefully
handled paths; with a retry budget of 2 every fault except the permanent
one is absorbed.
"""

NO_RETRY = {
    "timeout": "cascade",
    "transient": "graceful",
    "permanent": "cascade",
    "malformed": "silent-wrong",
    "partial-write": "cost-blowup",
    "duplicate": "graceful",
}

RETRY_BUDGET = 2


def outcome(fault: dict, retries: int) -> str:
    """Return the pipeline outcome for a fault.

    With a retry budget of 2 (retries >= 2) every fault except
    'permanent' resolves gracefully; without retries the fixed
    NO_RETRY table applies.
    """
    ftype = fault["type"]
    if retries >= RETRY_BUDGET and ftype != "permanent":
        return "graceful"
    if retries >= RETRY_BUDGET and ftype == "permanent":
        return "cascade"
    return NO_RETRY[ftype]
