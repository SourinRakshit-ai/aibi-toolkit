"""Build small demo models for tests, docs and screenshots."""

import random


def sample_model(tables: int = 3, measures_per_table: int = 2, seed: int = 42) -> dict:
    """Deterministically generate a fake model for demos."""
    rng = random.Random(seed)
    dims = ["Customer", "Product", "Date"][: max(0, tables - 1)]
    model = {"tables": [], "relationships": []}
    for name in ["Sales", *dims][:tables]:
        t = {"name": name, "columns": [{"name": f"{name[:3].lower()}_id"}], "measures": []}
        for i in range(measures_per_table):
            m = {"name": f"Measure {i + 1}"}
            if rng.random() < 0.5:
                m["formatString"] = "#,0.00"
            t["measures"].append(m)
        model["tables"].append(t)
    for i in range(1, len(model["tables"])):
        model["relationships"].append({
            "fromTable": "Sales",
            "toTable": model["tables"][i]["name"],
            "isActive": True,
            "cardinality": "manyToOne",
        })
    return model


def sample_csv(path, rows: int = 20, seed: int = 42) -> int:
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
