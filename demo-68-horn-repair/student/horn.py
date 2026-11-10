"""Minimum Horn-clause deletion that restores consistency (stdlib only)."""

import itertools


def closure(facts, clauses):
    derived = set(facts)
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            if all(atom in derived for atom in clause["body"]):
                head = clause["head"]
                if head is None:
                    return derived, True
                if head not in derived:
                    derived.add(head)
                    changed = True
    return derived, False


def is_inconsistent(facts, clauses):
    _, bad = closure(facts, clauses)
    return bad


def min_deletion(facts, clauses):
    """Smallest set of clause indices whose removal restores consistency."""
    n = len(clauses)
    if not is_inconsistent(facts, clauses):
        return [], False
    for k in range(1, n + 1):
        for subset in itertools.combinations(range(n), k):
            kept = [clause for i, clause in enumerate(clauses) if i not in subset]
            if not is_inconsistent(facts, kept):
                return list(subset), True
    return list(range(n)), True
