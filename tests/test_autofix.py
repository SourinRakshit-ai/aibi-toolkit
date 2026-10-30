from aibi_toolkit.autofix import fix_measure_name, suggest_format, autofix_model


def test_fix_measure_name():
    assert fix_measure_name("total sales amount ") == "Total Sales Amount"


def test_suggest_format():
    assert suggest_format("ASP = DIVIDE([Sales], [Units], 0)") == "#,0"


def test_autofix_model():
    model = {"tables": [{"name": "S", "measures": [{"name": "total_2", "expression": "SUM()"}]}]}
    r = autofix_model(model)
    assert r["count"] >= 1
    assert model["tables"][0]["measures"][0]["formatString"] == "$#,0.00"
