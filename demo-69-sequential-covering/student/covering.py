"""Sequential covering for a binary decision list (stdlib only)."""


def precision(rows, feature, positive_label):
    fired = [row for row in rows if row["features"].get(feature) == 1]
    if not fired:
        return 0.0, 0
    hits = sum(1 for row in fired if row["label"] == positive_label)
    return hits / len(fired), len(fired)


def learn(rows, positive_label):
    remaining = list(rows)
    unused = sorted({key for row in rows for key in row["features"]})
    rules = []
    while remaining and unused:
        ranked = []
        for feature in unused:
            prec, support = precision(remaining, feature, positive_label)
            ranked.append((prec, support, feature))
        prec, support, feature = max(ranked)
        if prec <= 0 or support == 0:
            break
        rules.append({"feature": feature, "label": positive_label, "precision": prec, "support": support})
        unused.remove(feature)
        remaining = [row for row in remaining if row["features"].get(feature) != 1]
    default = 1 - positive_label
    if remaining:
        pos = sum(1 for row in remaining if row["label"] == positive_label)
        default = positive_label if pos > len(remaining) / 2 else (1 - positive_label)
    return rules, default


def predict_one(features, rules, default):
    for rule in rules:
        if features.get(rule["feature"]) == 1:
            return rule["label"]
    return default


def accuracy(rows, rules, default):
    if not rows:
        return 1.0
    hits = sum(1 for row in rows if predict_one(row["features"], rules, default) == row["label"])
    return hits / len(rows)
