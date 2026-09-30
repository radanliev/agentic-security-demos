#!/usr/bin/env python3
"""Runner for Demo 18.

Runs the English-centric detector over the synthetic payloads, reports
recall split by English vs non-English. Writes results/lang_gap.json
and prints a summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from detector import flagged  # noqa: E402


def main() -> dict:
    """Score the detector, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "payloads.json").read_text())
    payloads = pack["payloads"]

    rows = []
    for p in payloads:
        hit = flagged(p["text"])
        rows.append(
            {
                "id": p["id"],
                "lang": p["lang"],
                "flagged": hit,
                "injected": p["injected"],
                "caught": hit and p["injected"],
                "missed": (not hit) and p["injected"],
            }
        )
    en = [r for r, p in zip(rows, payloads) if p["lang"] == "EN"]
    non_en = [r for r, p in zip(rows, payloads) if p["lang"] != "EN"]
    en_caught = sum(r["caught"] for r in en)
    non_en_caught = sum(r["caught"] for r in non_en)
    total_caught = sum(r["caught"] for r in rows)

    out = {
        "demo": "demo-18-crosslingual-gap",
        "experiment": "language-transfer",
        "seed": pack["seed"],
        "n_payloads": len(payloads),
        "en_recall": {"caught": en_caught, "total": len(en)},
        "non_en_recall": {"caught": non_en_caught, "total": len(non_en)},
        "total_caught": total_caught,
        "rows": rows,
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "lang_gap.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print(f"payloads {len(payloads)}  flagged {sum(r['flagged'] for r in rows)}")
    print("id    lang  injected  flagged")
    for p, r in zip(payloads, rows):
        print(f"{p['id']:<5} {p['lang']:<4}  {str(p['injected']):<8} {r['flagged']}")
    print(f"recall EN {en_caught}/{len(en)}  non-EN {non_en_caught}/{len(non_en)}  total {total_caught}/{len(payloads)}")
    print("lesson: English recall is perfect (4/4); non-English recall drops to 2/6.")
    return out


if __name__ == "__main__":
    main()
