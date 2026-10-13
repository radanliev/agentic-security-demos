"""Exact hypergeometric null for localisation claims (stdlib only).

At fixed pool P, defect count D and budget k, recall / precision / F1 are
strictly increasing functions of the same true-positive count TP, so every
threshold event is {TP >= t} and the null is the hypergeometric upper tail.
"""

import math


def tail(pool, defective, budget, observed):
    """P[TP >= observed] under random sampling without replacement."""
    if not (0 <= defective <= pool and 0 <= budget <= pool):
        raise ValueError("need 0 <= D <= P and 0 <= k <= P")
    if not (0 <= observed <= min(budget, defective)):
        if observed > min(budget, defective):
            return 0.0
        raise ValueError("observed TP out of range")
    total = math.comb(pool, budget)
    num = sum(
        math.comb(defective, i) * math.comb(pool - defective, budget - i)
        for i in range(observed, min(budget, defective) + 1)
    )
    return num / total


def scores(defective, budget, tp):
    """Return (recall, precision, f1) for a TP count."""
    recall = tp / defective if defective else 0.0
    precision = tp / budget if budget else 0.0
    denom = tp + defective + (budget - tp)
    f1 = 2 * tp / denom if denom else 0.0
    return recall, precision, f1


def lift(pool, defective, budget, tp):
    """Ratio-to-null: TP / E[TP]. Shown in the demo to be incomparable."""
    expected = defective * budget / pool if pool else 0.0
    return tp / expected if expected else 0.0


def required_pool(defective, budget, alpha=0.01):
    """Smallest pool P where even perfect TP=min(k,D) clears alpha.

    Returns None if no pool up to 10000 clears it (should not happen here).
    """
    cap = min(budget, defective)
    for pool in range(defective, 10001):
        if tail(pool, defective, budget, cap) <= alpha:
            return pool
    return None
