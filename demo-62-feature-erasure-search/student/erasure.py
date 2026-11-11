"""Minimum-cost feature-erasure search for a linear score (stdlib only)."""

import itertools


def score(weights, x, bias):
    return bias + sum(w * v for w, v in zip(weights, x))


def apply_erasure(x, indices):
    out = list(x)
    for i in indices:
        out[i] = 0.0
    return out


def exhaustive_min_erasure(weights, x, bias):
    """Smallest set of indices whose erasure flips the sign of the score."""
    original = score(weights, x, bias)
    if original == 0:
        return [], original
    n = len(weights)
    for k in range(0, n + 1):
        for subset in itertools.combinations(range(n), k):
            new = score(weights, apply_erasure(x, subset), bias)
            if original > 0 and new <= 0:
                return list(subset), new
            if original < 0 and new >= 0:
                return list(subset), new
    return None, original


def greedy_erasure(weights, x, bias):
    """Erase features in decreasing order of signed contribution until a flip."""
    original = score(weights, x, bias)
    if original == 0:
        return [], original
    order = sorted(
        range(len(weights)),
        key=lambda i: weights[i] * x[i] * (1 if original > 0 else -1),
        reverse=True,
    )
    chosen = []
    current = list(x)
    for i in order:
        chosen.append(i)
        current[i] = 0.0
        new = score(weights, current, bias)
        if original > 0 and new <= 0:
            return chosen, new
        if original < 0 and new >= 0:
            return chosen, new
    return None, original
