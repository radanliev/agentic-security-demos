#!/usr/bin/env python3
"""Deterministic epidemic spread toy for Demo 16.

Spread is a breadth-first flood from node 0: every reachable neighbour is
infected. There is no randomness; the per-edge probability p from the
fixtures is descriptive only and feeds the R0 illustration.
"""


def r0(p: float, degrees: list) -> float:
    """Return p times the mean degree."""
    if not degrees:
        return 0.0
    return p * (sum(degrees) / len(degrees))


def degrees_of(nodes: int, edges: list) -> list:
    """Return the undirected degree of each node."""
    degrees = [0] * nodes
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    return degrees


def _normalise_blocked(blocked_edges) -> set:
    """Normalise blocked edges to unordered pairs."""
    blocked = set()
    if not blocked_edges:
        return blocked
    for u, v in blocked_edges:
        blocked.add(frozenset((u, v)))
    return blocked


def simulate(nodes: int, edges: list, blocked_edges=None) -> set:
    """Deterministic BFS from node 0 infecting all neighbours.

    Edges in blocked_edges (containment) are never traversed.
    """
    blocked = _normalise_blocked(blocked_edges)
    adjacency: dict = {i: [] for i in range(nodes)}
    for u, v in edges:
        if frozenset((u, v)) in blocked:
            continue
        adjacency[u].append(v)
        adjacency[v].append(u)
    infected = {0}
    frontier = [0]
    while frontier:
        current = frontier.pop(0)
        for neighbour in adjacency[current]:
            if neighbour not in infected:
                infected.add(neighbour)
                frontier.append(neighbour)
    return infected
