#!/usr/bin/env python3
"""Capability tally for Demo 21.

Counts capability classes and shell/network bundling over server manifests.
"""

from collections import Counter


def tally(servers: list) -> dict:
    """Return capability counts, shell/network bundling, maintainer stats."""
    cap_counts: Counter = Counter()
    n_shell = 0
    n_shell_with_network = 0
    for s in servers:
        caps = s.get("capabilities", [])
        cap_counts.update(caps)
        if "shell" in caps:
            n_shell += 1
            if "network" in caps:
                n_shell_with_network += 1
    by_downloads = sorted(servers, key=lambda s: s["downloads"], reverse=True)
    top4 = by_downloads[:4]
    top4_maintainers = sorted({s["maintainer"] for s in top4})
    return {
        "capability_counts": dict(cap_counts),
        "n_shell": n_shell,
        "n_shell_with_network": n_shell_with_network,
        "top4_ids": [s["id"] for s in top4],
        "top4_maintainers": top4_maintainers,
    }
