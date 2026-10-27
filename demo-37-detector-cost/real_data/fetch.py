#!/usr/bin/env python3
"""Fetch a public Hugging Face dataset split as JSONL via the datasets-server rows API (stdlib only)."""
import json, sys, urllib.request, urllib.parse, time

def fetch(dataset, split, config="default", out=None):
    rows, off = [], 0
    while True:
        q = urllib.parse.urlencode({"dataset": dataset, "config": config, "split": split, "offset": off, "length": 100})
        for attempt in range(5):
            try:
                with urllib.request.urlopen("https://datasets-server.huggingface.co/rows?" + q, timeout=60) as r:
                    d = json.load(r); break
            except Exception:
                time.sleep(2 + attempt * 3)
        else:
            raise SystemExit("fetch failed")
        rows += [x["row"] for x in d["rows"]]
        off += 100
        if off >= d["num_rows_total"]:
            break
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)

if __name__ == "__main__":
    print(fetch(sys.argv[1], sys.argv[2], out=sys.argv[3]))
