#!/usr/bin/env python3
"""Toolflow taint helpers for Demo 44.

Finds flows that reach a sensitive sink without a provenance label.
Sensitive sinks are code, shell, file, network and memory; next-args is
the non-sensitive sink. All edges are synthetic teaching fixtures.
"""

SENSITIVE = ("code", "shell", "file", "network", "memory")


def unlabelled_to_sensitive(flows: list) -> list:
    """Return ids of unlabelled flows into sensitive sinks."""
    return [f["id"] for f in flows
            if not f["provenance"] and f["sink"] in SENSITIVE]
