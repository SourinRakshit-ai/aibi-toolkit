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
