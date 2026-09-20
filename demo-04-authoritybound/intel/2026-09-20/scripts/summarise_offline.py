#!/usr/bin/env python3
"""Offline schema + diagnostic summary for demo-4 external pulls.

No OpenRouter / no live model calls. Reads local artifacts under
artifacts/external_data/ and prints Markdown tables to stdout (and optional --out).
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

# AgentDojo banking static partition (offline D3 proxy; not the paper's 74-tool oracle).
BANKING_SIDE_EFFECTING = {
    "send_money",
    "schedule_transaction",
    "update_scheduled_transaction",
    "update_password",
    "update_user_info",
}
BANKING_READ_ONLY = {
    "get_balance",
    "get_iban",
    "get_most_recent_transactions",
    "get_scheduled_transactions",
    "get_user_info",
    "read_file",
}


def _tool_name(tc: dict) -> str | None:
    fn = tc.get("function")
    if isinstance(fn, str):
        return fn
    if isinstance(fn, dict):
        return fn.get("name")
    return tc.get("name")


def extract_tools(messages: list) -> list[str]:
    tools: list[str] = []
    for m in messages or []:
        for tc in m.get("tool_calls") or []:
            name = _tool_name(tc)
            if name:
                tools.append(name)
    return tools


def load_agentdojo(root: Path) -> list[dict]:
    rows: list[dict] = []
    for p in root.rglob("*.json"):
        if ".cache" in p.parts:
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if "suite_name" not in d:
            continue
        tools = extract_tools(d.get("messages") or [])
        rows.append(
            {
                "model": d.get("pipeline_name"),
                "suite": d.get("suite_name"),
                "user_task": d.get("user_task_id"),
                "inj_task": d.get("injection_task_id"),
                "attack": d.get("attack_type"),
                "utility": d.get("utility"),
                "security": d.get("security"),
                "tools": tools,
                "n_tools": len(tools),
                "benchmark_version": d.get("benchmark_version"),
                "path": str(p.relative_to(root)),
            }
        )
    return rows


def md_table(headers: list[str], rows: list[list]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for r in rows:
        lines.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(lines)


def summarise_agentdojo(rows: list[dict]) -> str:
    out: list[str] = []
    out.append("## AgentDojo trajectories (banking subset)")
    out.append("")
    out.append(f"- **Trajectory JSON count:** {len(rows)}")
    models = Counter(r["model"] for r in rows)
    attacks = Counter(r["attack"] for r in rows)
    out.append(
        f"- **Pipelines:** {', '.join(f'{k}={v}' for k, v in sorted(models.items()))}"
    )
    out.append(
        f"- **Suites in subset:** {sorted(set(r['suite'] for r in rows))}"
    )
    vers = Counter(r["benchmark_version"] for r in rows)
    out.append(f"- **benchmark_version:** {dict(vers)}")
    out.append("")
    out.append("### Schema / outcome counts")
    out.append("")
    util = Counter(r["utility"] for r in rows)
    sec = Counter(r["security"] for r in rows)
    out.append(
        md_table(
            ["Field", "Value", "Count"],
            [["utility", str(k), v] for k, v in util.most_common()]
            + [["security", str(k), v] for k, v in sec.most_common()]
            + [["attack_type", str(k), v] for k, v in attacks.most_common()],
        )
    )
    out.append("")
    out.append("### Attack × security (ASR proxy: security=False under attack)")
    out.append("")
    xs = Counter((r["attack"], r["security"]) for r in rows)
    rows_xs = []
    for attack in sorted({a for a, _ in xs}, key=lambda x: (x is None, str(x))):
        n_true = xs.get((attack, True), 0)
        n_false = xs.get((attack, False), 0)
        n = n_true + n_false
        asr = (n_false / n) if n else 0.0
        rows_xs.append([attack, n, n_true, n_false, f"{asr:.1%}"])
    out.append(
        md_table(
            ["attack_type", "n", "security=True", "security=False", "ASR proxy"],
            rows_xs,
        )
    )
    out.append("")
    out.append("### Per-pipeline utility / security")
    out.append("")
    per = []
    for model in sorted(models):
        sub = [r for r in rows if r["model"] == model]
        u = sum(1 for r in sub if r["utility"] is True)
        s = sum(1 for r in sub if r["security"] is True)
        per.append([model, len(sub), u, len(sub) - u, s, len(sub) - s])
    out.append(
        md_table(
            ["pipeline", "n", "utility=T", "utility=F", "security=T", "security=F"],
            per,
        )
    )
    out.append("")
    out.append("### Harness-decidable diagnostic summary (offline proxies)")
    out.append("")
    out.append(
        "These are **trajectory-dump proxies** for demo-4 diagnostics D1–D6. "
        "They do **not** re-run the paper’s capability mediator or shipped detector."
    )
    out.append("")

    clean = [r for r in rows if r["attack"] in (None, "none")]
    attacked = [r for r in rows if r["attack"] not in (None, "none")]
    clean_sec_t = sum(1 for r in clean if r["security"] is True)
    zero_tool = sum(1 for r in rows if r["n_tools"] == 0)
    zero_tool_atk = sum(1 for r in attacked if r["n_tools"] == 0)

    # D3: observed tool partition
    tool_counts = Counter(t for r in rows for t in r["tools"])
    se_calls = sum(tool_counts[t] for t in BANKING_SIDE_EFFECTING)
    ro_calls = sum(tool_counts[t] for t in BANKING_READ_ONLY)
    other = sum(
        c
        for t, c in tool_counts.items()
        if t not in BANKING_SIDE_EFFECTING | BANKING_READ_ONLY
    )
    se_tools_seen = sorted(t for t in tool_counts if t in BANKING_SIDE_EFFECTING)
    ro_tools_seen = sorted(t for t in tool_counts if t in BANKING_READ_ONLY)

    # D6 proxy: utility destruction under attack vs clean
    clean_util_f = sum(1 for r in clean if r["utility"] is False)
    atk_util_f = sum(1 for r in attacked if r["utility"] is False)

    # D4 proxy: fixture injection keys present
    # (re-scan lightly only for attacked with injections — already have inj_task)
    with_inj = sum(1 for r in rows if r["inj_task"])

    diag_rows = [
        [
            "D1 decidability",
            f"Clean (attack=None) episodes: {len(clean)}; "
            f"security=True among clean: {clean_sec_t}/{len(clean)} "
            f"(vacuous security on no-injection runs is harness-decidable). "
            f"Attacked episodes: {len(attacked)} — outcomes are model-dependent; "
            f"cannot recompute paper’s ‘attacker call never offered’ share without "
            f"AgentDojo ground_truth insertion into the proposal stream.",
        ],
        [
            "D2 denial-reason",
            "N/A on this dump: trajectories record tool/message traces and "
            "utility/security flags, not monitor denial reason codes.",
        ],
        [
            "D3 tool partition",
            f"Observed banking tools in subset: {len(tool_counts)} unique. "
            f"Static offline partition — side-effecting calls: {se_calls} "
            f"({', '.join(se_tools_seen) or 'none'}); read-only calls: {ro_calls} "
            f"({', '.join(ro_tools_seen) or 'none'}); unclassified calls: {other}. "
            f"Not the paper’s 29/74 suite-wide oracle.",
        ],
        [
            "D4 provenance labels",
            f"Episodes with injection_task_id set: {with_inj}/{len(rows)}. "
            f"Payloads arrive as fixture `injections` fields in the dump "
            f"(fixture-labelled), not as monitor-derived taint from executed traces.",
        ],
        [
            "D5 audit-log fidelity",
            "N/A: no monitor audit log / denial records in the public trajectory JSON.",
        ],
        [
            "D6 cost under attack",
            f"utility=False: clean {clean_util_f}/{len(clean)}; "
            f"attacked {atk_util_f}/{len(attacked)}. "
            f"Zero-tool trajectories: {zero_tool} overall "
            f"({zero_tool_atk} attacked) — early stops / empty tool traces "
            f"(cost channel incomplete without monitor timing).",
        ],
    ]
    out.append(md_table(["Diagnostic", "Offline finding on this dump"], diag_rows))
    out.append("")
    out.append("### Tool call frequency (banking subset)")
    out.append("")
    out.append(
        md_table(
            ["tool", "calls", "partition"],
            [
                [
                    t,
                    c,
                    (
                        "side-effecting"
                        if t in BANKING_SIDE_EFFECTING
                        else "read-only"
                        if t in BANKING_READ_ONLY
                        else "unclassified"
                    ),
                ]
                for t, c in tool_counts.most_common()
            ],
        )
    )
    return "\n".join(out)


def summarise_nemotron(path: Path) -> str:
    rows = [json.loads(l) for l in path.open()]
    out: list[str] = []
    out.append("## Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1")
    out.append("")
    out.append(f"- **Rows:** {len(rows)}")
    out.append(f"- **Source file:** `{path.name}`")
    domains = Counter(r["domain"] for r in rows)
    cats = Counter(r["attack_category"] for r in rows)
    targets = Counter(r["target_tool"] for r in rows)
    used = Counter(tuple(r.get("used_in") or []) for r in rows)
    vectors = Counter(r.get("injection_vector") for r in rows)
    out.append("")
    out.append("### Partition by domain")
    out.append("")
    out.append(
        md_table(
            ["domain", "n", "%"],
            [
                [d, n, f"{100 * n / len(rows):.1f}%"]
                for d, n in domains.most_common()
            ]
            + [["**total**", len(rows), "100%"]],
        )
    )
    out.append("")
    out.append("### Partition by attack_category (labels present)")
    out.append("")
    out.append(
        md_table(
            ["attack_category", "n", "%"],
            [
                [c, n, f"{100 * n / len(rows):.1f}%"]
                for c, n in cats.most_common()
            ]
            + [["**total**", len(rows), "100%"]],
        )
    )
    out.append("")
    out.append("### Partition by injection_vector")
    out.append("")
    out.append(
        md_table(
            ["injection_vector", "n"],
            [[v, n] for v, n in vectors.most_common()],
        )
    )
    out.append("")
    out.append("### Target tools (injection write targets)")
    out.append("")
    out.append(
        md_table(
            ["target_tool", "n"],
            [[t, n] for t, n in targets.most_common()],
        )
    )
    out.append("")
    out.append("### Other labels")
    out.append("")
    out.append(
        md_table(
            ["Field", "Observation"],
            [
                [
                    "used_in",
                    ", ".join(f"{k}={v}" for k, v in used.items()),
                ],
                [
                    "verifier_config",
                    "all rows: type=trace_analysis, mode=agentic_ipi "
                    "(deterministic resist/follow at *eval* time; "
                    "no resist/follow label column in the JSONL itself)",
                ],
                [
                    "required_tools",
                    "read tools that surface the injection "
                    f"({len(Counter(tuple(r.get('required_tools') or []) for r in rows))} distinct tuples)",
                ],
                [
                    "resist/follow outcome",
                    "NOT present as a row label — dataset retains successful "
                    "red-team injections for RL; outcome appears only when a "
                    "policy is rolled out against the verifier",
                ],
            ],
        )
    )
    # Cross tab domain x category
    out.append("")
    out.append("### Domain × attack_category")
    out.append("")
    cats_list = [c for c, _ in cats.most_common()]
    headers = ["domain"] + cats_list + ["total"]
    xt = []
    for d, _ in domains.most_common():
        row = [d]
        total = 0
        for c in cats_list:
            n = sum(
                1 for r in rows if r["domain"] == d and r["attack_category"] == c
            )
            row.append(n)
            total += n
        row.append(total)
        xt.append(row)
    out.append(md_table(headers, xt))
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repo root containing artifacts/external_data",
    )
    ap.add_argument("--out", type=Path, default=None, help="Optional Markdown sink")
    args = ap.parse_args()
    ext = args.root / "artifacts" / "external_data"
    agent_root = ext / "agentdojo-trajectories"
    nem_path = (
        ext
        / "Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1"
        / "train.jsonl"
    )

    parts = [
        "# Offline external-data summary",
        "",
        f"Root: `{args.root}`",
        "",
        "Generated by `scripts/external_data/summarise_offline.py` "
        "(no OpenRouter; local files only).",
        "",
    ]
    if agent_root.is_dir():
        rows = load_agentdojo(agent_root)
        parts.append(summarise_agentdojo(rows))
        parts.append("")
    else:
        parts.append(f"**Missing:** `{agent_root}`")
        parts.append("")
    if nem_path.is_file():
        parts.append(summarise_nemotron(nem_path))
        parts.append("")
    else:
        parts.append(f"**Missing:** `{nem_path}`")
        parts.append("")

    parts.append("## What NOT to claim")
    parts.append("")
    parts.append(
        "- Do not present these exploratory external baselines as the paper’s "
        "confirmatory primary sealed empirics."
    )
    parts.append(
        "- Do not claim Mac `.env` access, OpenRouter runs, or live monitor "
        "re-measurement from this offline dump pass."
    )
    parts.append(
        "- Do not equate trajectory `security=False` ASR proxies with the "
        "paper’s capability-mediator ASR under a reference monitor."
    )
    parts.append(
        "- Do not claim Nemotron rows are labelled resisted/followed; they are "
        "RL prompts with deterministic verifier *config*, not scored rollouts."
    )
    parts.append(
        "- Banking-only AgentDojo subset does not support suite-wide claims "
        "over slack/travel/workspace."
    )
    text = "\n".join(parts) + "\n"
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)


if __name__ == "__main__":
    main()
