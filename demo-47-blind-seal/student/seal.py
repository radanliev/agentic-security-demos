"""Pre-reveal seal for a localisation commitment (stdlib only).

The assessor writes a defect id. That text is hashed and chained before any
ground truth is read. Scoring accepts the guess only when the sealed bytes
still match; an edit after the seal is a mismatch, not a new answer.
"""

import hashlib
import json


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def seal(case_id, commitment, prev="0" * 64):
    body = commitment.strip()
    link = {
        "case_id": case_id,
        "commitment_sha256": digest(body),
        "prev": prev,
    }
    link["seal"] = digest(json.dumps(link, sort_keys=True))
    return link


def score(link, commitment, truth):
    """Return a verdict. Ground truth is consulted only after the seal matches."""
    if digest(commitment.strip()) != link["commitment_sha256"]:
        return "commitment_hash_mismatch"
    if commitment.strip() == truth:
        return "hit"
    return "miss"
