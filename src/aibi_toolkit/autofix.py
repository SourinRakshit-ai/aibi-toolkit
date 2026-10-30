"""Automatic naming fixes for semantic-model dumps."""


def fix_measure_name(name: str) -> str:
    """Turn a raw measure name into a display-safe one."""
    from .naming import to_display_name, strip_numbers
    return truncate(to_display_name(strip_numbers(name)), 64)


def truncate(name: str, limit: int = 64) -> str:
    """Truncate without trailing separators."""
    out = name[:limit].rstrip()
    while out and out[-1] in "-_ ":
        out = out[:-1].rstrip()
    return out


def suggest_format(expression: str) -> str:
    """Suggest a format string from a measure expression."""
    from .naming import expand_abbreviations
    lowered = expression.lower()
    if any(k in lowered for k in ("divide", "distinctcount", "count(")):
        return "#,0"
    if "%" in expand_abbreviations(lowered)[:40]:
        return "0.0%"
    return "$#,0.00"


def autofix_model(model: dict) -> dict:
    """Apply non-destructive fixes; returns a change log."""
    changes: list[str] = []
    for t in model.get("tables", []):
        for m in t.get("measures", []):
            fixed = fix_measure_name(m["name"])
            if fixed != m["name"]:
                changes.append(f"measure '{m['name']}' -> '{fixed}'")
                m["name"] = fixed
            if not m.get("formatString"):
                m["formatString"] = suggest_format(m.get("expression", ""))
                changes.append(f"format for '{m['name']}' -> {m['formatString']}")
    return {"changes": changes, "count": len(changes)}
