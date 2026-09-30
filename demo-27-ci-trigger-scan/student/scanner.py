#!/usr/bin/env python3
"""CI-trigger vulnerability predicate for Demo 27.

A repo is vulnerable when a public trigger can run a workflow with
write permission and no required review.
"""


def is_vulnerable(repo: dict) -> bool:
    """Return True when the repo wiring is injectable."""
    return (
        repo.get("public_trigger") is True
        and repo.get("permission") == "write"
        and repo.get("review_required") is False
    )
