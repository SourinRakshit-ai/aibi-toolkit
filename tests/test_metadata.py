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


def test_hidden_objects():
    from aibi_toolkit.metadata import hidden_objects
    model = {"tables": [{"name": "H", "isHidden": True, "columns": [{"name": "c", "isHidden": True}]}]}
    assert hidden_objects(model) == ["table:H", "column:c"]


def test_calculated_columns():
    from aibi_toolkit.metadata import calculated_columns
    model = {"tables": [{"name": "T", "columns": [{"name": "c", "type": "calculated", "expression": "1+1"}]}]}
    assert calculated_columns(model)[0]["expression"] == "1+1"
