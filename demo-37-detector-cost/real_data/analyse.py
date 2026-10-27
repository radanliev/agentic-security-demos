#!/usr/bin/env python3
"""Score the two Demo 37 rule detectors on the public deepset/prompt-injections corpus.

Real data, not synthetic. The detectors are still the toy substring rules; the
numbers describe these rules on this corpus only, not any production detector.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "student"))
from detectors import strict, lenient

HERE = Path(__file__).parent
rows = []
for f in ("deepset_train.jsonl", "deepset_test.jsonl"):
    rows += [json.loads(l) for l in open(HERE / f)]

def conf(fn):
    tp = sum(1 for r in rows if r["label"] == 1 and fn(r["text"]))
    fp = sum(1 for r in rows if r["label"] == 0 and fn(r["text"]))
    fn_ = sum(1 for r in rows if r["label"] == 1 and not fn(r["text"]))
    tn = sum(1 for r in rows if r["label"] == 0 and not fn(r["text"]))
    return dict(tp=tp, fp=fp, fn=fn_, tn=tn)

out = {"n": len(rows), "positives": sum(r["label"] for r in rows), "detectors": {}}
for name, fn in (("strict", strict), ("lenient", lenient)):
    c = conf(fn)
    c["cost_fp10_fn25"] = 10 * c["fp"] + 25 * c["fn"]
    c["recall"] = round(c["tp"] / (c["tp"] + c["fn"]), 4)
    c["fpr"] = round(c["fp"] / (c["fp"] + c["tn"]), 4)
    out["detectors"][name] = c
# cost-ratio sweep: FN cost / FP cost from 0.25 to 10
sweep = []
for ratio in (0.25, 0.5, 1, 2, 2.5, 5, 10):
    s = {k: v["fp"] + ratio * v["fn"] for k, v in out["detectors"].items()}
    sweep.append({"fn_over_fp": ratio, **{k: round(v, 2) for k, v in s.items()}, "cheaper": min(s, key=s.get)})
out["sweep"] = sweep
json.dump(out, open(HERE / "results.json", "w"), indent=2)
print(json.dumps(out, indent=2))
