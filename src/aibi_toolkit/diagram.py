"""Mermaid ER-diagram export of model relationships."""


def mermaid_er(model: dict) -> str:
    """Render relationships as a mermaid erDiagram block."""
    lines = ["erDiagram"]
    for r in model.get("relationships", []):
        f = _safe(r.get("fromTable", "?"))
        t = _safe(r.get("toTable", "?"))
        lines.append(f"    {f} ||--o{{ {t} : has")
    return "\n".join(lines)


def _safe(name: str) -> str:
    return name.replace(" ", "_") or "Unknown"


def mermaid_tables(model: dict, limit: int = 20) -> str:
    """Render the first N tables as a mermaid graph for top-level shape."""
    lines = ["graph TD"]
    for i, t in enumerate(model.get("tables", [])[:limit]):
        lines.append(f"    T{i}[{_safe(t['name'])}]")
    for r in model.get("relationships", []):
        names = [x["name"] for x in model.get("tables", [])]
        if r.get("fromTable") in names and r.get("toTable") in names:
            lines.append(f"    T{names.index(r['fromTable'])} --> T{names.index(r['toTable'])}")
    return "\n".join(lines)
