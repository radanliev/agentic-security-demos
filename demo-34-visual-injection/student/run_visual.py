#!/usr/bin/env python3
"""Evaluator for Demo 34.

Compares a baseline that acts on all typographic content against a
region defense that ignores the untrusted region.

Writes results/visual.json and prints the summary table.
"""

import json
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DEMO_DIR / "student"))

from visual import baseline_success, injections, region_defense  # noqa: E402


def main() -> dict:
    """Evaluate baseline and defense, write results, print table."""
    pack = json.loads((DEMO_DIR / "fixtures" / "images.json").read_text())
    images = pack["images"]
    inj_ids = injections(images)
    base = baseline_success(images)
    defense = region_defense(images)
    out = {
        "demo": "demo-34-visual-injection",
        "experiment": "visual-injection",
        "seed": pack["seed"],
        "total": len(images),
        "injections": base["injections"],
        "injection_ids": inj_ids,
        "baseline_acted": base["acted"],
        "blocked_injections": len(defense["blocked_injections"]),
        "blocked_injection_ids": defense["blocked_injections"],
        "blocked_benign": len(defense["blocked_benign"]),
        "blocked_benign_ids": defense["blocked_benign"],
        "notes": "Synthetic teaching fixture",
    }
    (DEMO_DIR / "results").mkdir(exist_ok=True)
    (DEMO_DIR / "results" / "visual.json").write_text(
        json.dumps(out, indent=2) + "\n"
    )

    print("id   typographic  region     acted")
    for image in sorted(images, key=lambda i: i["id"]):
        print(f"{image['id']}   {str(image['typographic']):<12} {image['region']:<10} {str(image['acted'])}")
    print(f"baseline injections acted {base['acted']}/{base['injections']}")
    print(f"defense blocked {len(defense['blocked_injections'])}/{base['injections']} injections, benign cost {len(defense['blocked_benign'])}")
    return out


if __name__ == "__main__":
    main()
