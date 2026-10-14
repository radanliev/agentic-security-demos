# Demo 46 — Execution Instructions

```bash
python3 -m pytest tests/ -v
python3 student/run_drift.py
```

Expected: 4 tests passed. The small swap stays under the frozen mean 0.1222. The orthogonal swap is flagged above it.
