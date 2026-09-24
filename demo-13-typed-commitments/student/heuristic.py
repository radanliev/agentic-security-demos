#!/usr/bin/env python3
"""Shared toy heuristic for Demo 13.

Both toy assessors fall back to this rule when they have no cue to follow:
nominate the file containing a suspicious token (``password`` or ``exec(``);
if none matches, nominate the lexicographically-first file.

It is deliberately weak so the exercise can show cue-following overriding it.
"""

from typing import Dict

SUSPICIOUS_TOKENS = ("password", "exec(")


def heuristic_pick(files: Dict[str, str]) -> str:
    """Pick one filename from a {filename: content} mapping."""
    for name in sorted(files):
        content = files[name]
        if any(tok in content for tok in SUSPICIOUS_TOKENS):
            return name
    return sorted(files)[0]
