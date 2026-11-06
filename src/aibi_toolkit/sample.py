"""Build small demo models for tests, docs and screenshots."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any

from .metadata import Model


def sample_model(tables: int = 3, measures_per_table: int = 2, seed: int = 42) -> Model:
    """Deterministically generate a fake model for demos."""
    rng = random.Random(seed)
    dims = ["Customer", "Product", "Date"][: max(0, tables - 1)]
    tables_list: list[dict[str, Any]] = []
    for name in ["Sales", *dims][:tables]:
        t: dict[str, Any] = {
            "name": name,
            "columns": [{"name": f"{name[:3].lower()}_id"}],
            "measures": [],
        }
        for i in range(measures_per_table):
            m: dict[str, Any] = {"name": f"Measure {i + 1}"}
            if rng.random() < 0.5:
                m["formatString"] = "#,0.00"
            t["measures"].append(m)
        tables_list.append(t)
    relationships = [
        {
            "fromTable": "Sales",
            "toTable": tables_list[i]["name"],
            "isActive": True,
            "cardinality": "manyToOne",
        }
        for i in range(1, len(tables_list))
    ]
    return {"tables": tables_list, "relationships": relationships}


def sample_csv(path: str | Path, rows: int = 20, seed: int = 42) -> int:
    """Write a demo measures CSV; returns row count."""
    from .csvio import export_measures
    rng = random.Random(seed)
    rows_data = [
        {
            "table": rng.choice(["Sales", "Customer", "Product"]),
            "name": f"Measure {n}",
            "expression": "SUM()",
            "formatString": "" if n % 3 else "#,0",
        }
        for n in range(1, rows + 1)
    ]
    return export_measures(rows_data, path)
