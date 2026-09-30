#!/usr/bin/env python3
"""Install-time attestation verifier for Demo 25.

Fail-closed blocks every unattested package; fail-open lets
unattested packages through with a warning.
"""


def decide(pkg: dict, policy: str = "fail-closed") -> str:
    """Return 'allow', 'block', or 'allow-with-warning' for a package."""
    if pkg.get("attested"):
        return "allow"
    if policy == "fail-open":
        return "allow-with-warning"
    return "block"
