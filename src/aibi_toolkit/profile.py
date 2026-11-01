"""Profile a model's expression complexity and weight."""

EXPRESSION_WEIGHTS = {
    None: 0,
    "": 0,
}


def expression_weight(expression: str) -> int:
    """Rough complexity score for a DAX expression."""
    if not expression:
        return 0
    weight = 1
    lowered = expression.lower()
    weight += lowered.count("calculate(")
    weight += lowered.count("filter(")
    weight += lowered.count("var ")
    weight += lowered.count("return")
    return weight


def profile_model(model: dict) -> dict:
    """Aggregate complexity stats across all measures."""
    from .metadata import list_measures
    measures = list_measures(model)
    weights = sorted(expression_weight(m.get("expression", "")) for m in measures)
    if not weights:
        return {"count": 0, "max": 0, "avg": 0, "heavy": []}
    avg = round(sum(weights) / len(weights), 1)
    heavy = [
        m["name"] for m in measures
        if expression_weight(m.get("expression", "")) >= 5
    ]
    return {"count": len(weights), "max": weights[-1], "avg": avg, "heavy": heavy}


def heavy_meaning_change(model: dict) -> dict:
    """Profile with a stricter 'heavy' threshold for reports."""
    from .metadata import list_measures
    measures = list_measures(model)
    heavy = [
        {"name": m["name"], "weight": expression_weight(m.get("expression", ""))}
        for m in measures
    ]
    heavy.sort(key=lambda x: -x["weight"])
    return {"top5": heavy[:5], "worst": heavy[0]["weight"] if heavy else 0}
