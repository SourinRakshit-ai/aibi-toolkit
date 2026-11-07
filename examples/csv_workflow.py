"""Demo 2: the CSV round-trip — export, edit, diff two inventories.

Run from the repo root: python examples/csv_workflow.py
"""

import tempfile
from pathlib import Path

from aibi_toolkit.csvio import diff_inventories, summarize_csv
from aibi_toolkit.sample import sample_csv


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        week1 = Path(tmp) / "week1.csv"
        week2 = Path(tmp) / "week2.csv"

        sample_csv(str(week1), rows=8)
        sample_csv(str(week2), rows=10, seed=43)  # superset with different rows

        print("week 1:", summarize_csv(week1))
        print("week 2:", summarize_csv(week2))

        changes = diff_inventories(week1, week2)
        print(f"added:   {len(changes['added'])}")
        print(f"removed: {len(changes['removed'])}")
        print(f"changed: {len(changes['changed'])}")
        for key in changes["changed"][:3]:
            print(f"  changed: {key}")


if __name__ == "__main__":
    main()
