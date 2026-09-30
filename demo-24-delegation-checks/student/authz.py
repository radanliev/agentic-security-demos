#!/usr/bin/env python3
"""Delegation-property checks for Demo 24.

Two properties over a delegation chain:

- audience binding: every hop must name the same audience.
- no amplification: scope must not increase along the chain.
"""


def check(chain: dict) -> list:
    """Return a list of violation strings (empty when clean)."""
    violations = []
    hops = chain["hops"]
    audiences = [h["audience"] for h in hops]
    if len(set(audiences)) > 1:
        violations.append(
            f"audience-mismatch: expected all '{audiences[0]}' got {audiences}"
        )
    for i in range(1, len(hops)):
        if hops[i]["scope"] > hops[i - 1]["scope"]:
            violations.append(
                f"scope-amplification at hop {i}: "
                f"{hops[i - 1]['scope']}->{hops[i]['scope']}"
            )
    return violations
