"""Deterministic technique-to-control alignment (stdlib only)."""


def recommend(techniques, alignment):
    """Return sorted union of controls aligned to known techniques."""
    controls = set()
    unknown = []
    uncovered = []
    for tech in techniques:
        mapped = alignment.get(tech)
        if mapped is None:
            unknown.append(tech)
            uncovered.append(tech)
            continue
        if not mapped:
            uncovered.append(tech)
        controls.update(mapped)
    return {
        "controls": sorted(controls),
        "unknown": unknown,
        "uncovered": uncovered,
        "covered": [t for t in techniques if t not in uncovered],
    }
