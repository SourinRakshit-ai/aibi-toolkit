"""Model relationship integrity checks."""


def check_relationships(model: dict) -> dict:
    """Find inactive and many-to-many unsafe relationships."""
    out = {"inactive": [], "bidirectional": []}
    for r in model.get("relationships", []):
        label = f"{r.get('fromTable')} -> {r.get('toTable')}"
        if not r.get("isActive", True):
            out["inactive"].append(label)
        if r.get("crossFilterDirection") == "both":
            out["bidirectional"].append(label)
    return out
