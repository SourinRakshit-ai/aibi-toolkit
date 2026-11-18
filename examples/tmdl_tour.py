"""Demo 2: point aibi at a TMDL folder and audit it end to end.

Run from the repo root: python examples/tmdl_tour.py
Uses the same fixture layout snapshot tests use.
"""

from pathlib import Path

from aibi_toolkit.audit import audit_measures, audit_score
from aibi_toolkit.metadata import list_measures, list_tables, load_model

FIXTURE = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "pbip"


def main() -> None:
    model = load_model(str(FIXTURE))
    print(f"tables: {list_tables(model)}")
    print("measures:")
    for m in list_measures(model):
        fmt = m.get("formatString")
        print(f"  {m['table']:<10} {m['name']:<25} format={fmt}")
    print()
    findings = audit_measures(model)
    for category, names in findings.items():
        for name in names:
            print(f"  [{category}] {name}")
    print(f"score: {audit_score(model)}/100")


if __name__ == "__main__":
    main()
