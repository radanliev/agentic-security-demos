"""Run the demo 51 equity audit over the synthetic placeholder scores and write results/guardrail_equity.json."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "student"))

from guardrail_equity import disparity, fit_thresholds, paired_flip_rate, rates  # noqa: E402


def main() -> int:
    fixture = json.loads((ROOT / "fixtures" / "synthetic_scores.json").read_text(encoding="utf-8"))
    records, global_threshold = fixture["records"], fixture["global_threshold"]
    table = rates(records, global_threshold)
    ratios = disparity(table)
    flips = paired_flip_rate(records, global_threshold)
    print("Demo 51: guardrail equity audit across writing variants (synthetic placeholder scores)\n")
    print(f"Global threshold {global_threshold}")
    print(f"{'variant':28} {'FPR':>6} {'TPR':>6} {'ratio':>7} {'flips':>6}")
    for variant in sorted(table):
        row = table[variant]
        flip = flips.get(variant)
        print(
            f"{variant:28} {row['fpr']:6.2f} {row['tpr']:6.2f} {ratios[variant]:7.2f} "
            f"{('-' if flip is None else f'{flip:.2f}'):>6}"
        )
    thresholds, conflicts = fit_thresholds(records, global_threshold, target_fpr=0.25, recall_floor=0.9)
    print("\nAudit-only per-variant thresholds (target FPR 0.25, detection floor 0.90):")
    for variant, t in thresholds.items():
        note = "  conflict: floor not met, global threshold kept" if variant in conflicts else ""
        print(f"  {variant:28} {t:.2f}{note}")
    out = ROOT / "results" / "guardrail_equity.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "global_threshold": global_threshold,
        "variants": table,
        "disparity": ratios,
        "paired_flip_rate": flips,
        "audit_thresholds": thresholds,
        "conflicts": conflicts,
    }, indent=2) + "\n")
    print("\nScores are placeholders that exercise the audit; they are not results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
