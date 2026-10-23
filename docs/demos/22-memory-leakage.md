# Demo 22: Memory Leakage

## Learning Objectives

- Explain the three memory-privacy failure modes: persisting high-sensitivity content, resurfacing entries across sessions/users, and failing to honour deletion
- Run a tiny leakage screen over 8 synthetic memory entries and read its counts
- Distinguish memory PRIVACY (leakage: what is kept, reshown, or not erased) from memory INTEGRITY (poisoning: what is planted), the topic of the sibling Demo 28
- Distinguish this teaching toy from the pending study it illustrates (no data collected there yet)

## Conceptual Explanation

Agents with persistent memory can leak in three quiet ways: they store content they should not keep, they resurface one session's content in another session or user, and they keep content the user asked to delete.

This toy uses 8 hand-built entries:

| Check | Result | Lesson |
|-------|--------|--------|
| Persists high-sensitivity (`m1`, `m2`) | 2 | high-sensitivity content should never persist |
| Resurfaces across sessions (`m3`, `m4`) | 2 | entries reappear under another session/user |
| Erasure failures (`m7` of 3 deleted) | 1/3 | deletion is requested but the entry stays |

Entries `m5`/`m6` are the contrast: deleted and actually gone.

Boundary: this demo is memory leakage (privacy); memory poisoning (integrity) is Demo 28. Different question, data, and claims.

## Safety Notice

⚠️ **Teaching demonstration only.**
- No real memory stores, users, sessions, or personal data
- No network access (standard library only)
- All entries and verdicts are hand-built toys

## Run It

```bash
cd demo-22-memory-leakage
python3 -m pytest tests/ -v          # 6 tests, <1 min
python3 student/run_memory.py        # writes results/memory_leak.json
```

Full step-by-step: [Execution Instructions](https://github.com/radanliev/agentic-security-demos/blob/main/demo-22-memory-leakage/INSTRUCTIONS.md).
