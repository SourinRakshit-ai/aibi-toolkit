from aibi_toolkit.audit import audit_measures, audit_score

MODEL = {
    "tables": [
        {
            "name": "Sales",
            "measures": [
                {"name": "Total", "formatString": "#,0"},
                {"name": "total"},
                {"name": "x" * 70},
            ],
        }
    ]
}


def test_audit_measures():
    f = audit_measures(MODEL)
    assert "total" in f["duplicate_names"]
    assert "Total" not in f["missing_format"]
    assert f["long_names"]


def test_audit_score():
    assert 0 <= audit_score(MODEL) <= 100
