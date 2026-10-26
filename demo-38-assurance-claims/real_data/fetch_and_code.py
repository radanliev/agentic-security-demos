#!/usr/bin/env python3
"""Fetch the 60 most-downloaded public text-generation model cards on Hugging Face and
keyword-code them against the five Demo 38 obligations.

Real public data. The coding is an automated keyword heuristic, NOT the study's
present/absent/vague human codebook; treat it as a screening pass only.
"""
import json, re, urllib.request, urllib.parse, time
from pathlib import Path
H = Path(__file__).parent
RULES = {
    "threats": r"\b(risk|risks|misuse|harm|harmful|threat)",
    "evals": r"\b(evaluat\w*|benchmark\w*)",
    "agentic": r"\b(agent\w*|tool[- ]use|tool[- ]calling|function[- ]calling)",
    "third_party": r"(third[- ]party|external red[- ]team\w*|independent (evaluat\w*|audit\w*|red[- ]team\w*))",
    "mitigations": r"\b(mitigat\w*|guardrail\w*|safety (tuning|training|filter\w*)|content filter\w*|refus\w*)",
}
def get(url, raw=False):
    for a in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                b = r.read(); return b.decode("utf-8", "replace") if raw else json.loads(b)
        except Exception as e:
            err = e; time.sleep(2)
    return None
models = get("https://huggingface.co/api/models?" + urllib.parse.urlencode(
    {"pipeline_tag": "text-generation", "sort": "downloads", "direction": -1, "limit": 80}))
rows = []
for m in models:
    if len(rows) >= 60: break
    mid = m["id"]
    card = get(f"https://huggingface.co/{mid}/raw/main/README.md", raw=True)
    if not card or len(card) < 500:  # skip gated/empty cards
        continue
    low = card.lower()
    flags = {k: bool(re.search(p, low)) for k, p in RULES.items()}
    rows.append({"model": mid, "sha": m.get("sha"), "downloads": m.get("downloads"), "card_chars": len(card), **flags})
json.dump(rows, open(H / "cards_coded.json", "w"), indent=1)
n = len(rows)
summ = {"n_cards": n, "covered": {k: sum(r[k] for r in rows) for k in RULES},
        "all_five": sum(all(r[k] for k in RULES) for r in rows)}
json.dump(summ, open(H / "results.json", "w"), indent=2)
print(json.dumps(summ, indent=2))
