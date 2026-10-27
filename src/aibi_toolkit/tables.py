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
