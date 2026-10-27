#!/usr/bin/env python3
"""Apply the Demo 40 union -> SHA-256 dedupe -> licence gate pipeline to four public prompt corpora.

Real public data. Licence classes come from each dataset card's licence field as
retrieved on 26 Oct 2026; a missing field is treated as 'unlicensed' (blocked).
"""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "student"))
from corpus import digest, dedupe, ALLOWED

H = Path(__file__).parent
SOURCES = [  # (source id, files, text field, licence class)
    ("deepset", ["deepset_train.jsonl", "deepset_test.jsonl"], "text", "permissive"),
    ("jackhhao", ["jackhhao_train.jsonl", "jackhhao_test.jsonl"], "prompt", "permissive"),
    ("lakera", ["lakera_train.jsonl", "lakera_validation.jsonl", "lakera_test.jsonl"], "text", "permissive"),
    ("rubend18", ["rubend18_train.jsonl"], "Prompt", "unlicensed"),
]
recs = []
for sid, files, field, lic in SOURCES:
    for f in files:
        for line in open(H / f):
            r = json.loads(line)
            if r.get(field):
                recs.append({"source": sid, "text": r[field], "license": lic})
ingested = Counter(r["source"] for r in recs)
within = {s: ingested[s] - len({digest(r["text"]) for r in recs if r["source"] == s}) for s in ingested}
uniq = dedupe(recs)
srcsets = {}
for r in recs:
    srcsets.setdefault(digest(r["text"]), set()).add(r["source"])
cross = Counter(tuple(sorted(v)) for v in srcsets.values() if len(v) > 1)
released = [r for r in uniq if r["license"] in ALLOWED]
out = {
    "ingested_total": len(recs), "ingested_by_source": dict(ingested),
    "within_source_duplicates": within, "unique_after_dedupe": len(uniq),
    "digests_in_multiple_sources": {"+".join(k): v for k, v in cross.items()},
    "releasable": len(released), "blocked_unlicensed": len(uniq) - len(released),
    "unique_by_first_source": dict(Counter(r["source"] for r in uniq)),
}
json.dump(out, open(H / "results.json", "w"), indent=2)
print(json.dumps(out, indent=2))
