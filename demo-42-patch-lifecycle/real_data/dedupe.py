#!/usr/bin/env python3
"""Collapse OSV records that are aliases of one another (GHSA preferred), then recompute lag statistics into results.json."""
import json, statistics
rows = json.load(open("advisories.json")); seen = set(); u = []
for r in sorted(rows, key=lambda r: (not r["id"].startswith("GHSA"), r["id"])):
    k = {r["pkg"] + ":" + x for x in [r["id"]] + r["aliases"]}
    if k & seen: continue
    seen |= k; u.append(r)
l = [r["lag_days"] for r in u if "lag_days" in r]
o = json.load(open("results.json"))
o["alias_deduplicated"] = {"advisories": len(u), "with_fix_and_dates": len(l), "median_lag_days": statistics.median(l),
    "advisory_before_fix": sum(x < 0 for x in l), "within_7d": sum(0 <= x <= 7 for x in l), "over_90d": sum(x > 90 for x in l),
    "no_fixed_version": sum(1 for r in u if not r["fixed"])}
json.dump(o, open("results.json", "w"), indent=2); print(o["alias_deduplicated"])
