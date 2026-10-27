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
