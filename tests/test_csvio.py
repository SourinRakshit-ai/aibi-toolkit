from aibi_toolkit.csvio import export_measures, import_measures


def test_roundtrip(tmp_path):
    rows = [{"table": "Sales", "name": "Total", "expression": "SUM()", "formatString": "#,0"}]
    p = tmp_path / "m.csv"
    export_measures(rows, p)
    assert import_measures(p) == rows


def test_diff(tmp_path):
    from aibi_toolkit.csvio import diff_inventories
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    export_measures([{"table": "S", "name": "T1", "expression": "1", "formatString": ""}], a)
    export_measures([{"table": "S", "name": "T2", "expression": "1", "formatString": ""}], b)
    d = diff_inventories(a, b)
    assert d["added"] == [("S", "T2")]
    assert d["removed"] == [("S", "T1")]
