"""Name normalization helpers for tables, columns and measures."""

import re


def to_snake_case(name: str) -> str:
    """Convert a human-readable name to snake_case."""
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return re.sub(r"\s+", "_", name.strip()).lower()


def to_display_name(name: str) -> str:
    """Convert snake_case or camelCase to a Title Case display name."""
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    name = name.replace("_", " ").strip()
    return " ".join(w.capitalize() for w in name.split())


ABBREVIATIONS = {
    "qty": "quantity",
    "amt": "amount",
    "cust": "customer",
    "rev": "revenue",
    "ytd": "year to date",
}


def expand_abbreviations(name: str, mapping: dict | None = None) -> str:
    """Expand common BI abbreviations to their full words."""
    mapping = mapping or ABBREVIATIONS
    words = name.replace("_", " ").split()
    return " ".join(mapping.get(w.lower(), w) for w in words)


def sanitize_table_name(name: str) -> str:
    """Remove characters that break Power BI / SQL identifiers."""
    name = re.sub(r"[^\w\s()-]", "", name)
    return re.sub(r"\s+", " ", name).strip()
