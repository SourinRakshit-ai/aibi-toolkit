from aibi_toolkit.metadata import list_measures, model_summary

MODEL = {
    "tables": [
        {"name": "Sales", "measures": [{"name": "Total"}], "columns": [{"name": "A"}, {"name": "B"}]},
        {"name": "Dim", "measures": [], "columns": [{"name": "C"}]},
    ]
}


def test_list_measures():
    assert list_measures(MODEL)[0]["table"] == "Sales"


def test_summary():
    s = model_summary(MODEL)
    assert s == {"tables": 2, "measures": 1, "columns": 3}
