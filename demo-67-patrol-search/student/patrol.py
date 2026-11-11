"""Search for a k-node patrol allocation that covers attacker paths (stdlib only)."""

import itertools


def uncovered(paths, chosen):
    chosen = set(chosen)
    return sum(1 for path in paths if chosen.isdisjoint(path))


def exhaustive(nodes, paths, k):
    """Return a k-subset with the fewest uncovered paths (ties: lexicographic)."""
    if k <= 0:
        return [], uncovered(paths, [])
    if k >= len(nodes):
        chosen = list(nodes)
        return chosen, uncovered(paths, chosen)
    best = None
    best_score = None
    for subset in itertools.combinations(sorted(nodes), k):
        score = uncovered(paths, subset)
        if best_score is None or score < best_score:
            best = list(subset)
            best_score = score
    return best, best_score


def greedy(nodes, paths, k):
    """Repeatedly add the node that covers the most still-uncovered paths."""
    chosen = []
    remaining = list(paths)
    unused = set(nodes)
    for _ in range(min(k, len(nodes))):
        def covers(node):
            return sum(1 for path in remaining if node in path)
        node = min(unused, key=lambda n: (-covers(n), n))
        chosen.append(node)
        unused.remove(node)
        remaining = [path for path in remaining if node not in path]
        if not remaining:
            break
    return chosen, uncovered(paths, chosen)
