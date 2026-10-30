"""Plain-text table rendering for CLI output."""


def markdown_table(rows: list[dict], columns: list[str] | None = None) -> str:
    """Render rows as a GitHub-flavored markdown table."""
    if not rows:
        return ""
    columns = columns or list(rows[0].keys())
    widths = [max(len(str(c)), *(len(str(r.get(c, ""))) for r in rows)) for c in columns]
    header = "| " + " | ".join(c.ljust(w) for c, w in zip(columns, widths)) + " |"
    sep = "| " + " | ".join("-" * w for w in widths) + " |"
    body = [
        "| " + " | ".join(str(r.get(c, "")).ljust(w) for c, w in zip(columns, widths)) + " |"
        for r in rows
    ]
    return "\n".join([header, sep, *body])


def align_column(rows: list[dict], column: str, right: bool = False) -> list[dict]:
    """Pad a column's values for aligned plain-text output."""
    width = max((len(str(r.get(column, ""))) for r in rows), default=0)
    return [
        {**r, column: str(r.get(column, "")).rjust(width) if right else str(r.get(column, "")).ljust(width)}
        for r in rows
    ]


def plain_table(rows: list[dict], columns: list[str] | None = None) -> str:
    """Render rows as a bordered plain-text table for terminals."""
    if not rows:
        return ""
    columns = columns or list(rows[0].keys())
    widths = [max(len(str(c)), *(len(str(r.get(c, ""))) for r in rows)) for c in columns]
    header = " ".join(str(c).ljust(w) for c, w in zip(columns, widths))
    sep = "-" * len(header)
    lines = [header, sep]
    for r in rows:
        lines.append(" ".join(str(r.get(c, "")).ljust(w) for c, w in zip(columns, widths)))
    return "\n".join(lines)
