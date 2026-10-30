from aibi_toolkit.diagram import mermaid_er


def test_er():
    model = {"relationships": [{"fromTable": "Sales", "toTable": "Dim"}]}
    out = mermaid_er(model)
    assert out.startswith("erDiagram")
    assert "Sales ||--o{ Dim" in out
