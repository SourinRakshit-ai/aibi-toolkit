from aibi_toolkit.integrity import check_relationships, check_cardinality

MODEL = {
    "relationships": [
        {"fromTable": "Sales", "toTable": "Dim", "isActive": False},
        {"fromTable": "A", "toTable": "B", "crossFilterDirection": "both"},
        {"fromTable": "C", "toTable": "D", "cardinality": "manyToOne"},
    ]
}


def test_check_relationships():
    r = check_relationships(MODEL)
    assert r["inactive"] == ["Sales -> Dim"]
    assert r["bidirectional"] == ["A -> B"]


def test_cardinality():
    assert check_cardinality(MODEL) == ["Sales -> Dim", "A -> B"]


def test_orphans():
    from aibi_toolkit.integrity import orphan_tables
    model = {
        "relationships": [{"fromTable": "A", "toTable": "B"}],
        "tables": [
            {"name": "A", "columns": [{"name": "x"}]},
            {"name": "B", "columns": []},
            {"name": "Lone", "columns": [{"name": "y"}]},
            {"name": "Hidden", "columns": []},
        ],
    }
    assert orphan_tables(model) == ["Lone"]
