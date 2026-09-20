#!/usr/bin/env python3
"""CPU triage baseline on slim EMBER 2018 shard sample (sklearn + xgboost).

SEPARATION: malware PE-feature triage only — no demo-11 IPI/Nemotron/boundary-pairs.
No OpenRouter / LLM calls.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    roc_auc_score,
)
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "artifacts" / "external_data" / "ember2018-malware" / "data"
OUT = ROOT / "artifacts" / "ember_baseline"
OUT.mkdir(parents=True, exist_ok=True)

# Slim sample: mixed train shards (shard 1 is all-benign early years) + one test shard.
TRAIN_SHARDS = [
    DATA / "ember2018_train_50.jsonl",
    DATA / "ember2018_train_100.jsonl",
]
TEST_SHARDS = [DATA / "ember2018_test_1.jsonl"]

MAX_TRAIN = 12000
MAX_TEST = 4000
RANDOM_STATE = 42


def parse_label(row: dict) -> int | None:
    """Return 0/1; skip unlabeled (-1) and unknowns."""
    for key in ("label", "y"):
        v = row.get(key)
        if v is None:
            continue
        if isinstance(v, (int, float)):
            iv = int(v)
            if iv in (0, 1):
                return iv
            return None  # -1 unlabeled etc.
        s = str(v).strip().lower()
        if s in {"0", "0.0", "benign", "false"}:
            return 0
        if s in {"1", "1.0", "malware", "malicious", "true"}:
            return 1
        if s in {"-1", "-1.0", "nan", "none", ""}:
            return None
        try:
            iv = int(float(s))
            if iv in (0, 1):
                return iv
        except ValueError:
            pass
    return None


def features_from_row(row: dict) -> np.ndarray | None:
    x = row.get("x")
    if isinstance(x, list) and len(x) > 0:
        try:
            return np.asarray(x, dtype=np.float32)
        except (TypeError, ValueError):
            return None
    inp = row.get("input")
    if isinstance(inp, str) and inp.strip():
        parts = inp.replace(",", " ").split()
        try:
            return np.asarray([float(p) for p in parts], dtype=np.float32)
        except ValueError:
            return None
    return None


def load_jsonl_files(paths: list[Path], max_rows: int) -> tuple[np.ndarray, np.ndarray, dict]:
    xs: list[np.ndarray] = []
    ys: list[int] = []
    skipped = {"unlabeled_or_bad": 0, "no_feat": 0, "bad_dim": 0}
    dim = None
    per_file = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        before = len(ys)
        with path.open() as f:
            for line in f:
                if len(xs) >= max_rows:
                    break
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                lab = parse_label(row)
                if lab is None:
                    skipped["unlabeled_or_bad"] += 1
                    continue
                feat = features_from_row(row)
                if feat is None:
                    skipped["no_feat"] += 1
                    continue
                if dim is None:
                    dim = int(feat.shape[0])
                if feat.shape[0] != dim:
                    skipped["bad_dim"] += 1
                    continue
                xs.append(feat)
                ys.append(lab)
        per_file.append(
            {
                "path": str(path.name),
                "bytes": path.stat().st_size,
                "n_kept_from_file": int(len(ys) - before),
            }
        )
        if len(xs) >= max_rows:
            break
    X = np.stack(xs) if xs else np.zeros((0, 0), dtype=np.float32)
    y = np.asarray(ys, dtype=np.int32)
    meta = {
        "files": per_file,
        "n_loaded": int(len(y)),
        "n_pos": int((y == 1).sum()) if len(y) else 0,
        "n_neg": int((y == 0).sum()) if len(y) else 0,
        "feature_dim": int(dim or 0),
        "skipped": skipped,
        "max_rows_cap": max_rows,
    }
    return X, y, meta


def metrics_bundle(y_true, y_prob, y_pred) -> dict:
    out = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": None,
        "average_precision": None,
    }
    if len(np.unique(y_true)) > 1:
        out["roc_auc"] = float(roc_auc_score(y_true, y_prob))
        out["average_precision"] = float(average_precision_score(y_true, y_prob))
    return out


def main() -> None:
    t0 = time.perf_counter()
    X_train, y_train, train_meta = load_jsonl_files(TRAIN_SHARDS, MAX_TRAIN)
    X_test, y_test, test_meta = load_jsonl_files(TEST_SHARDS, MAX_TEST)

    if len(np.unique(y_train)) < 2:
        raise SystemExit(f"train has <2 classes: {train_meta}")
    if len(np.unique(y_test)) < 2:
        raise SystemExit(f"test has <2 classes: {test_meta}")

    X_train = np.nan_to_num(X_train, nan=0.0, posinf=0.0, neginf=0.0)
    X_test = np.nan_to_num(X_test, nan=0.0, posinf=0.0, neginf=0.0)

    scaler = StandardScaler()
    Xtr = scaler.fit_transform(X_train)
    Xte = scaler.transform(X_test)

    models = {}

    t = time.perf_counter()
    lr = LogisticRegression(max_iter=800, random_state=RANDOM_STATE)
    lr.fit(Xtr, y_train)
    prob = lr.predict_proba(Xte)[:, 1]
    pred = (prob >= 0.5).astype(int)
    models["logistic_regression"] = {
        **metrics_bundle(y_test, prob, pred),
        "fit_seconds": round(time.perf_counter() - t, 3),
    }

    t = time.perf_counter()
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        n_jobs=-1,
        random_state=RANDOM_STATE,
        class_weight="balanced_subsample",
    )
    rf.fit(X_train, y_train)
    prob = rf.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.5).astype(int)
    models["random_forest"] = {
        **metrics_bundle(y_test, prob, pred),
        "fit_seconds": round(time.perf_counter() - t, 3),
        "n_estimators": 200,
    }

    t = time.perf_counter()
    hgb = HistGradientBoostingClassifier(
        max_depth=8,
        learning_rate=0.1,
        max_iter=150,
        random_state=RANDOM_STATE,
    )
    hgb.fit(X_train, y_train)
    prob = hgb.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.5).astype(int)
    models["hist_gradient_boosting"] = {
        **metrics_bundle(y_test, prob, pred),
        "fit_seconds": round(time.perf_counter() - t, 3),
    }

    t = time.perf_counter()
    xgb = XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="auc",
        tree_method="hist",
        device="cpu",
        n_jobs=-1,
        random_state=RANDOM_STATE,
    )
    xgb.fit(X_train, y_train)
    prob = xgb.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.5).astype(int)
    models["xgboost"] = {
        **metrics_bundle(y_test, prob, pred),
        "fit_seconds": round(time.perf_counter() - t, 3),
        "n_estimators": 200,
        "device": "cpu",
        "tree_method": "hist",
    }

    catalog_path = (
        ROOT
        / "artifacts"
        / "external_data"
        / "malware-families-catalog"
        / "malware_families.parquet"
    )
    catalog_meta = None
    if catalog_path.exists():
        import pandas as pd

        cat = pd.read_parquet(catalog_path)
        catalog_meta = {
            "path": str(catalog_path),
            "bytes": catalog_path.stat().st_size,
            "n_rows": int(len(cat)),
            "columns_sample": list(cat.columns)[:12],
            "n_families": int(cat["family"].nunique()) if "family" in cat.columns else None,
        }

    best = max(
        models.items(),
        key=lambda kv: (kv[1]["roc_auc"] is not None, kv[1]["roc_auc"] or -1),
    )

    payload = {
        "run_id": "ember-baseline-slim-2026-09-20",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "timezone_note": "Europe/Skopje (UTC+2)",
        "hub_id": "cw1521/ember2018-malware",
        "citation_hint": "EMBER 2018 (Anderson & Roth / Elastic); HF mirror cw1521/ember2018-malware",
        "task": "binary malware vs benign PE-feature triage",
        "hardware": "CPU only (box)",
        "separation": {
            "demo11_ipi_excluded": True,
            "nemotron_excluded": True,
            "boundary_pairs_excluded": True,
            "openrouter_excluded": True,
            "note": "Malware triage baseline only; no demo-11 IPI/reporting datasets.",
        },
        "data_limits": {
            "full_hub_approx": "~400 train + ~100 test JSONL shards (~65–72 MB each; multi-tens-of-GB total)",
            "slim_sample_files": [p.name for p in TRAIN_SHARDS + TEST_SHARDS],
            "note_train_1_skipped": "ember2018_train_1.jsonl is early-year all-benign; kept on disk for documentation but not used in fit",
            "unlabeled_policy": "skip label/y == -1",
            "row_caps": {"max_train": MAX_TRAIN, "max_test": MAX_TEST},
            "not_full_ember_replication": True,
        },
        "train": train_meta,
        "test": test_meta,
        "models": models,
        "best_model_by_roc_auc": {"name": best[0], **best[1]},
        "malware_families_catalog": catalog_meta,
        "total_seconds": round(time.perf_counter() - t0, 3),
        "claim_level": "exploratory external CPU baseline — not confirmatory primary paper empirics",
    }

    out_path = OUT / "metrics.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"wrote": str(out_path), "best": payload["best_model_by_roc_auc"], "train": train_meta, "test": test_meta}, indent=2))


if __name__ == "__main__":
    main()
