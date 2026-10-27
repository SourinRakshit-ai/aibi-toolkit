"""Name normalization helpers for tables, columns and measures."""

import re


def to_snake_case(name: str) -> str:
    """Convert a human-readable name to snake_case."""
    name = re.sub(r"[^\w\s]", " ", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return re.sub(r"\s+", "_", name.strip()).lower()
