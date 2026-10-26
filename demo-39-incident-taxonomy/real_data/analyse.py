#!/usr/bin/env python3
"""Tally public AVID (AI Vulnerability Database) reports by SEP view, risk domain and
a keyword screen for the four Demo 39 attack patterns.

Real public data (MIT licence). Pass the path of a local avid-db clone:
    git clone --depth 1 https://github.com/avidml/avid-db /tmp/avid
    python3 analyse.py /tmp/avid
The pattern screen is a keyword heuristic, not expert coding.
"""
import json, re, sys
from collections import Counter
from pathlib import Path
root = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/avid")
PAT = {
    "prompt-injection": r"prompt injection|jailbreak|ignore (all |the )?(previous|prior) instructions|indirect injection",
    "tool-misuse": r"code execution|\brce\b|tool|plugin|sql injection|shell",
    "data-exfiltration": r"exfiltrat|leak|training data extraction|pii|personal data|memoriz",
    "privilege-escalation": r"privilege|escalat|unauthori[sz]ed access|bypass auth",
}
files = sorted(p for p in (root / "reports").rglob("*.json") if "review" not in p.parts)
sep, dom, pat, years = Counter(), Counter(), Counter(), Counter()
n = 0
for p in files:
    try: d = json.load(open(p))
    except Exception: continue
    n += 1
    years[p.parts[-2] if p.parts[-2].isdigit() else "?"] += 1
    imp = (d.get("impact") or {}).get("avid") or {}
    for s in imp.get("sep_view") or []: sep[s.split(":")[0]] += 1
    for r in imp.get("risk_domain") or []: dom[r] += 1
    text = " ".join(str((d.get(k) or {}).get("description", {}).get("value", "") if k == "problemtype" else (d.get(k) or {}).get("value", "")) for k in ("problemtype", "description")).lower()
    hit = [k for k, rx in PAT.items() if re.search(rx, text)]
    for h in hit: pat[h] += 1
    if not hit: pat["none-matched"] += 1
out = {"n_reports": n, "by_year_folder": dict(years), "risk_domain": dict(dom.most_common()),
       "sep_view_top10": dict(sep.most_common(10)), "pattern_screen_multilabel": dict(pat.most_common())}
json.dump(out, open(Path(__file__).parent / "results.json", "w"), indent=2)
print(json.dumps(out, indent=2))
