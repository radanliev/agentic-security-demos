#!/usr/bin/env python3
"""Sandbox escape-rate helpers for Demo 26."""


def escape_rate(matrix: dict, config: str) -> tuple:
    """Return (n_escaped, n_total, rate) for a sandbox config."""
    col = matrix["configs"][config]
    escaped = [p for p in matrix["probes"] if col[p]]
    total = len(matrix["probes"])
    return len(escaped), total, (len(escaped) / total if total else 0.0)


def escaped_probes(matrix: dict, config: str) -> list:
    """Return the probe names that escape under a config."""
    col = matrix["configs"][config]
    return [p for p in matrix["probes"] if col[p]]
