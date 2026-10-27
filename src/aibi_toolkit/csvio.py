"""CSV export/import of measure inventories."""

import csv
from pathlib import Path


def export_measures(measures: list[dict], path) -> int:
    """Write measures to CSV; returns the row count."""
    fieldnames = ["table", "name", "expression", "formatString"]
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for m in measures:
            w.writerow({k: m.get(k, "") for k in fieldnames})
    return len(measures)


REQUIRED_FIELDS = ("table", "name", "expression")


def import_measures(path) -> list[dict]:
    """Read measures from CSV, raising on rows missing required fields."""
    out = []
    with Path(path).open("r", newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            missing = [k for k in REQUIRED_FIELDS if not row.get(k)]
            if missing:
                raise ValueError(f"Row {i} missing required fields: {missing}")
            out.append(row)
    return out
