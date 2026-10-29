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


MEASURE_PREFIXES = {
    "count": "Count of",
    "sum": "Total",
    "avg": "Average",
    "ratio": "%",
}


def suggest_measure_prefix(aggregation: str) -> str:
    """Suggest a display prefix for a measure based on its aggregation."""
    return MEASURE_PREFIXES.get(aggregation.lower(), aggregation.capitalize() + " of")


def dedupe_names(names: list[str]) -> list[str]:
    """Ensure unique names by appending 2, 3, ... on conflicts."""
    seen, out = set(), []
    for n in names:
        base, i = n, 1
        while n.lower() in seen:
            i += 1
            n = f"{base} {i}"
        seen.add(n.lower())
        out.append(n)
    return out


def truncate_name(name: str, limit: int = 64) -> str:
    """Truncate a name to a character limit without trailing spaces."""
    return name[:limit].rstrip()


def normalize_all(names: list[str]) -> list[str]:
    """snake_case, de-abbreviate, then dedupe in one pass."""
    cleaned = [expand_abbreviations(to_snake_case(n)) for n in names]
    return dedupe_names(cleaned)


def pascal_case(name: str) -> str:
    """Convert any name style to PascalCase."""
    words = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name).replace("_", " ").split()
    return "".join(w.capitalize() for w in words)


def validate_name(name: str) -> list[str]:
    """Return a list of naming-violation messages (empty = clean)."""
    issues = []
    if name != name.strip():
        issues.append("leading/trailing whitespace")
    if "  " in name or "__" in name:
        issues.append("repeated separators")
    if len(name) > 64:
        issues.append("longer than 64 chars")
    return issues


def kebab_case(name: str) -> str:
    """Convert any name style to kebab-case."""
    words = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name).replace("_", " ").split()
    return "-".join(w.lower() for w in words)


def strip_numbers(name: str) -> str:
    """Remove numeric suffixes such as 'Table 2' -> 'Table'."""
    return re.sub(r"\s+\d+$", "", name).strip()


VOWELS = "aeiouAEIOU"


def a_or_an(word: str) -> str:
    """Return the correct article for a word."""
    return "an" if word and word[0] in VOWELS else "a"


def pluralize(word: str) -> str:
    """Naive pluralization for table names."""
    if word.endswith(("s", "x", "ch", "sh")):
        return word + "es"
    if word.endswith("y") and len(word) > 1 and word[-2] not in VOWELS:
        return word[:-1] + "ies"
    return word + "s"
