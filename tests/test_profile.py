from aibi_toolkit.profile import expression_weight, profile_model

DAX = "M =\nVAR _a = CALCULATE([X])\nRETURN _a"


def test_expression_weight():
    assert expression_weight(DAX) == 4  # VAR + CALCULATE + RETURN + base


def test_profile_empty():
    assert profile_model({"tables": []})["count"] == 0


def test_profile_flags_heavy():
    model = {"tables": [{"name": "T", "measures": [{"name": "Big", "expression": "CALCULATE(FILTER(CALCULATE(FILTER(1),1),1),1)"}]}]}
    assert "Big" in profile_model(model)["heavy"]


def test_weight_tier():
    from aibi_toolkit.profile import weight_tier
    assert weight_tier(1) == "light"
    assert weight_tier(4) == "medium"
    assert weight_tier(7) == "heavy"
