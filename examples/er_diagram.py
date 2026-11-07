"""Demo 3: render mermaid ER and table diagrams from a sample model.

Run from the repo root: python examples/er_diagram.py
"""

import tempfile
from pathlib import Path

from aibi_toolkit.diagram import mermaid_er, mermaid_tables
from aibi_toolkit.metadata import load_model
from aibi_toolkit.sample import sample_model


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "demo.json"
        path.write_text(__import__("json").dumps(sample_model(tables=4)), encoding="utf-8")
        model = load_model(str(path))

    print("```mermaid")
    print(mermaid_er(model))
    print("```")
    print()
    print("```mermaid")
    print(mermaid_tables(model, limit=4))
    print("```")


if __name__ == "__main__":
    main()
