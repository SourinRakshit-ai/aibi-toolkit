"""Model relationship integrity checks."""

from __future__ import annotations

from .metadata import Model


def check_relationships(model: Model) -> dict[str, list[str]]:
    """Find inactive and many-to-many unsafe relationships."""
    out: dict[str, list[str]] = {"inactive": [], "bidirectional": []}
    for r in model.get("relationships", []):
        label = f"{r.get('fromTable')} -> {r.get('toTable')}"
        if not r.get("isActive", True):
            out["inactive"].append(label)
        if r.get("crossFilterDirection") == "both":
            out["bidirectional"].append(label)
    return out


def check_cardinality(model: Model) -> list[str]:
    """Warn on relationships without declared cardinality."""
    return [
        f"{r.get('fromTable')} -> {r.get('toTable')}"
        for r in model.get("relationships", [])
        if not r.get("cardinality")
    ]


def orphan_tables(model: Model) -> list[str]:
    """Tables not connected to any relationship."""
    rel_tables: set[str] = set()
    for r in model.get("relationships", []):
        rel_tables.add(r.get("fromTable"))
        rel_tables.add(r.get("toTable"))
    return [
        t["name"] for t in model.get("tables", [])
        if t["name"] not in rel_tables and (t.get("columns") or t.get("measures"))
    ]


def role_playing_dimensions(model: Model) -> dict[str, list[str]]:
    """Detect a date/lookup table joined multiple times."""
    counts: dict[str, list[str]] = {}
    for r in model.get("relationships", []):
        to_table = r.get("toTable")
        counts.setdefault(to_table, []).append(r.get("fromTable", "?"))
    return {t: srcs for t, srcs in counts.items() if len(srcs) > 1}
