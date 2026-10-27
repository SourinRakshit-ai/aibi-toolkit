"""Load and inspect semantic-model metadata dumps (TMDL-exported JSON)."""

import json
from pathlib import Path


def load_model(path) -> dict:
    """Load a model JSON dump from disk."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data


def list_tables(model: dict) -> list[str]:
    """Return all table names in the model."""
    return [t["name"] for t in model.get("tables", [])]


def list_measures(model: dict, table: str | None = None) -> list[dict]:
    """List measures, optionally filtered to one table."""
    out = []
    for t in model.get("tables", []):
        if table and t["name"] != table:
            continue
        for m in t.get("measures", []):
            out.append({**m, "table": t["name"]})
    return out


def model_summary(model: dict) -> dict:
    """High-level counts for a quick model health glance."""
    tables = model.get("tables", [])
    return {
        "tables": len(tables),
        "measures": sum(len(t.get("measures", [])) for t in tables),
        "columns": sum(len(t.get("columns", [])) for t in tables),
    }


def find_unused_measures(model: dict) -> list[str]:
    """Best-effort scan for measures with no format string set."""
    return [
        m["name"]
        for t in model.get("tables", [])
        for m in t.get("measures", [])
        if not m.get("formatString")
    ]


def count_standalone_measures(model: dict) -> int:
    """Measures that live on tables with no columns (helper/measure tables)."""
    return sum(
        len(t.get("measures", []))
        for t in model.get("tables", [])
        if not t.get("columns")
    )
