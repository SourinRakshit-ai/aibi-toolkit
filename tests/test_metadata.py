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


def test_find_unused_measures():
    from aibi_toolkit.metadata import find_unused_measures
    model = {"tables": [{"name": "S", "measures": [{"name": "A"}, {"name": "B", "formatString": "#,0"}]}]}
    assert find_unused_measures(model) == ["A"]


def test_count_standalone():
    from aibi_toolkit.metadata import count_standalone_measures
    model = {"tables": [{"name": "M", "measures": [{"name": "x"}], "columns": []}, {"name": "S", "measures": [], "columns": [{"name": "c"}]}]}
    assert count_standalone_measures(model) == 1


def test_relationships():
    from aibi_toolkit.metadata import relationships
    model = {"relationships": [{"fromTable": "Sales", "toTable": "Dim", "isActive": True}]}
    assert relationships(model)[0]["from"] == "Sales"
