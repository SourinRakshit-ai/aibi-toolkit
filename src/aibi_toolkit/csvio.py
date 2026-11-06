"""CSV export/import of measure inventories."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

Measure = dict[str, Any]
MeasureKey = dict[tuple[str, str], Measure]
Row = dict[str, str]


def export_measures(measures: list[Measure], path: str | Path) -> int:
    """Write measures to CSV; returns the row count."""
    fieldnames = ["table", "name", "expression", "formatString"]
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for m in measures:
            w.writerow({k: m.get(k, "") for k in fieldnames})
    return len(measures)


REQUIRED_FIELDS = ("table", "name", "expression")


def import_measures(path: str | Path) -> list[Measure]:
    """Read measures from CSV, raising on rows missing required fields."""
    out: list[Measure] = []
    with Path(path).open("r", newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            missing = [k for k in REQUIRED_FIELDS if not row.get(k)]
            if missing:
                raise ValueError(f"Row {i} missing required fields: {missing}")
            out.append(dict(row))
    return out


def summarize_csv(path: str | Path) -> dict[str, int]:
    """Return basic stats about a measures CSV: rows and tables."""
    rows = import_measures(path)
    return {"rows": len(rows), "tables": len({r["table"] for r in rows})}


def diff_inventories(old_path: str | Path, new_path: str | Path) -> dict[str, Any]:
    """Compare two measure CSVs: added, removed, changed."""
    old: MeasureKey = {(r["table"], r["name"]): r for r in import_measures(old_path)}
    new: MeasureKey = {(r["table"], r["name"]): r for r in import_measures(new_path)}
    return {
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "changed": sorted(k for k in set(old) & set(new) if old[k] != new[k]),
    }
