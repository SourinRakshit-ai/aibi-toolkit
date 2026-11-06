"""Load and inspect semantic-model metadata dumps (TMDL-exported JSON)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

Model = dict[str, Any]
Measure = dict[str, Any]
Table = dict[str, Any]


def load_model(path: str) -> Model:
    """Load a model JSON dump from disk."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("model dump must be a JSON object")
    return data


def list_tables(model: Model) -> list[str]:
    """Return all table names in the model."""
    return [t["name"] for t in model.get("tables", [])]


def list_measures(model: Model, table: str | None = None) -> list[Measure]:
    """List measures, optionally filtered to one table."""
    out: list[Measure] = []
    for t in model.get("tables", []):
        if table and t["name"] != table:
            continue
        for m in t.get("measures", []):
            out.append({**m, "table": t["name"]})
    return out


def model_summary(model: Model) -> dict[str, int]:
    """High-level counts for a quick model health glance."""
    tables = model.get("tables", [])
    return {
        "tables": len(tables),
        "measures": sum(len(t.get("measures", [])) for t in tables),
        "columns": sum(len(t.get("columns", [])) for t in tables),
    }


def find_unused_measures(model: Model) -> list[str]:
    """Best-effort scan for measures with no format string set."""
    return [
        m["name"]
        for t in model.get("tables", [])
        for m in t.get("measures", [])
        if not m.get("formatString")
    ]


def count_standalone_measures(model: Model) -> int:
    """Measures that live on tables with no columns (helper/measure tables)."""
    return sum(
        len(t.get("measures", []))
        for t in model.get("tables", [])
        if not t.get("columns")
    )


def relationships(model: Model) -> list[dict[str, Any]]:
    """List model relationships in a readable form."""
    return [
        {"from": r.get("fromTable"), "to": r.get("toTable"), "active": r.get("isActive", True)}
        for r in model.get("relationships", [])
    ]


def hidden_objects(model: Model) -> list[str]:
    """List objects marked hidden in the model."""
    out: list[str] = []
    for t in model.get("tables", []):
        if t.get("isHidden"):
            out.append(f"table:{t['name']}")
        out.extend(f"column:{c['name']}" for c in t.get("columns", []) if c.get("isHidden"))
    return out


def calculated_columns(model: Model) -> list[dict[str, Any]]:
    """List calculated columns with their expressions."""
    return [
        {"table": t["name"], "name": c["name"], "expression": c.get("expression", "")}
        for t in model.get("tables", [])
        for c in t.get("columns", [])
        if c.get("type") == "calculated"
    ]
