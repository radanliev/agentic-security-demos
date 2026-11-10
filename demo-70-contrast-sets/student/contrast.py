"""Contrast-set growth rates across two bags of itemsets (stdlib only)."""

from collections import Counter


def item_support(windows):
    n = len(windows)
    counts = Counter()
    for bag in windows:
        for item in set(bag):
            counts[item] += 1
    if n == 0:
        return {}
    return {item: count / n for item, count in counts.items()}


def growth_rate(support_a, support_b):
    if support_a == 0:
        return float("inf") if support_b > 0 else 0.0
    return support_b / support_a


def emerging(window_a, window_b, min_support_b, min_growth):
    supp_a = item_support(window_a)
    supp_b = item_support(window_b)
    items = set(supp_a) | set(supp_b)
    rows = []
    flagged = []
    for item in sorted(items):
        a = supp_a.get(item, 0.0)
        b = supp_b.get(item, 0.0)
        growth = growth_rate(a, b)
        is_emerging = b >= min_support_b and growth >= min_growth
        row = {"item": item, "support_a": a, "support_b": b, "growth": growth, "emerging": is_emerging}
        rows.append(row)
        if is_emerging:
            flagged.append(item)
    return rows, flagged


def top_frequency(window_a, window_b, k):
    """Time-agnostic top-k items by combined support (baseline)."""
    combined = window_a + window_b
    supp = item_support(combined)
    ranked = sorted(supp, key=lambda item: (-supp[item], item))
    return ranked[:k]
