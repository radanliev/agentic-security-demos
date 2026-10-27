#!/usr/bin/env python3
"""Fix-to-advisory lag for public OSV advisories on major LLM-stack PyPI packages.

Real public data: OSV (https://osv.dev, CC-BY 4.0) and PyPI JSON release metadata.
For each advisory with a fixed version, lag_days = advisory published date minus
the upload date of the first fixed release. Negative = advisory before fix.
"""
import json, urllib.request, statistics, datetime as dt
from pathlib import Path
PKGS = ["langchain", "langchain-core", "langchain-community", "llama-index", "llama-index-core",
        "transformers", "vllm", "gradio", "mlflow", "litellm", "ray", "torch"]
def post(url, body):
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
def get(url):
    with urllib.request.urlopen(url, timeout=60) as r: return json.load(r)
def ts(s): return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
rows = []
for pkg in PKGS:
    vulns = post("https://api.osv.dev/v1/query", {"package": {"name": pkg, "ecosystem": "PyPI"}}).get("vulns", [])
    rel = get(f"https://pypi.org/pypi/{pkg}/json")["releases"]
    for v in vulns:
        fixed = [e["fixed"] for a in v.get("affected", []) if a.get("package", {}).get("name", "").lower() == pkg
                 for r in a.get("ranges", []) for e in r.get("events", []) if "fixed" in e]
        up = [min(ts(f["upload_time_iso_8601"]) for f in rel[x]) for x in fixed if rel.get(x)]
        row = {"pkg": pkg, "id": v["id"], "aliases": v.get("aliases", []), "published": v.get("published"), "fixed": fixed}
        if up and v.get("published"):
            row["fix_upload"] = min(up).isoformat()
            row["lag_days"] = (ts(v["published"]) - min(up)).days
        rows.append(row)
json.dump(rows, open(Path(__file__).parent / "advisories.json", "w"), indent=1)
lags = [r["lag_days"] for r in rows if "lag_days" in r]
out = {"advisories": len(rows), "with_fix_and_dates": len(lags), "no_fixed_version": sum(1 for r in rows if not r["fixed"]),
       "median_lag_days": statistics.median(lags) if lags else None,
       "advisory_before_fix": sum(l < 0 for l in lags), "advisory_within_7d_after_fix": sum(0 <= l <= 7 for l in lags),
       "advisory_over_90d_after_fix": sum(l > 90 for l in lags),
       "per_package": {p: sum(1 for r in rows if r["pkg"] == p) for p in PKGS}}
json.dump(out, open(Path(__file__).parent / "results.json", "w"), indent=2)
print(json.dumps(out, indent=2))
