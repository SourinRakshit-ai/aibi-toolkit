from aibi_toolkit.report import generate_report, write_report

MODEL = {
    "tables": [
        {"name": "Sales", "measures": [{"name": "Total", "formatString": "#,0"}],
         "columns": [{"name": "A"}]},
        {"name": "Empty", "columns": []},
    ],
    "relationships": [{"fromTable": "Sales", "toTable": "Empty", "isActive": False}],
}


def test_report_sections():
    r = generate_report(MODEL)
    for h in ("# Model Audit Report", "## Overview", "## Measure findings",
              "## Table findings", "## Relationship findings"):
        assert h in r


def test_write_report(tmp_path):
    p = tmp_path / "report.md"
    write_report(MODEL, p)
    assert p.exists()
