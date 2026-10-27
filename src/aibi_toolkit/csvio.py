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
