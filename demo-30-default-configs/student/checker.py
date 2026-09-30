#!/usr/bin/env python3
"""Default-config checker for Demo 30.

A stack is insecure when any of these hold:
  - it binds publicly without auth,
  - it runs privileged,
  - it pins a known-vulnerable dependency.
The function returns the list of reasons (empty means secure).
"""


def is_insecure(stack: dict) -> list:
    """Return the list of insecurity reasons for one stack."""
    reasons = []
    if stack.get("bind_public") and not stack.get("auth"):
        reasons.append("public-without-auth")
    if stack.get("privileged"):
        reasons.append("privileged")
    if stack.get("pinned_vuln"):
        reasons.append("pinned-vuln")
    return reasons


def check_all(stacks: list) -> dict:
    """Partition stacks into insecure and secure id lists."""
    insecure = [s["id"] for s in stacks if is_insecure(s)]
    secure = [s["id"] for s in stacks if not is_insecure(s)]
    pinned = [s["id"] for s in stacks if s.get("pinned_vuln") and is_insecure(s)]
    return {"insecure": sorted(insecure), "secure": sorted(secure), "pinned": sorted(pinned)}
