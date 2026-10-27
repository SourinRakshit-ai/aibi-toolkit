from aibi_toolkit.csvio import export_measures, import_measures


def test_roundtrip(tmp_path):
    rows = [{"table": "Sales", "name": "Total", "expression": "SUM()", "formatString": "#,0"}]
    p = tmp_path / "m.csv"
    export_measures(rows, p)
    assert import_measures(p) == rows
