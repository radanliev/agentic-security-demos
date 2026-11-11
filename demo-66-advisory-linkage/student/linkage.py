"""Exact-identifier linkage and severity / product disagreement (stdlib only)."""

import re


def tokens(text):
    return {part for part in re.split(r"[^a-z0-9]+", text.lower()) if part}


def jaccard(a, b):
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def link(source_a, source_b):
    by_id_b = {row["id"]: row for row in source_b}
    rows = []
    for left in source_a:
        right = by_id_b.get(left["id"])
        if right is None:
            rows.append({"id": left["id"], "matched": False, "severity_disagree": False, "product_disagree": False, "jaccard": None})
            continue
        jac = jaccard(tokens(left["product"]), tokens(right["product"]))
        rows.append({
            "id": left["id"], "matched": True,
            "severity_disagree": left["severity"] != right["severity"],
            "product_disagree": jac < 1.0, "jaccard": jac,
        })
    return rows
