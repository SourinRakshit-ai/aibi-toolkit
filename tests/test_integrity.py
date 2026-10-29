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
