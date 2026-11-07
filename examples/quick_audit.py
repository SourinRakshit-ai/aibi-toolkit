"""Demo 1: audit a model and print the hygiene score.

Run from the repo root: python examples/quick_audit.py
"""

import tempfile
from pathlib import Path

from aibi_toolkit.audit import audit_measures, audit_score
from aibi_toolkit.metadata import load_model
from aibi_toolkit.sample import sample_model


def main() -> None:
    # Generate a deterministic demo model rather than shipping a fixture.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "demo.json"
        path.write_text(__import__("json").dumps(sample_model(tables=3)), encoding="utf-8")

        model = load_model(str(path))
        findings = audit_measures(model)
        score = audit_score(model)

        print("Measures hygiene findings:")
        for category, names in findings.items():
            for name in names:
                print(f"  [{category}] {name}")
        print(f"score: {score}/100")


if __name__ == "__main__":
    main()
