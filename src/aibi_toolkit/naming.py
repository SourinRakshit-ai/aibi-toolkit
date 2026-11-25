from __future__ import annotations

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


def expand_abbreviations(name: str,  mapping: dict[str, str] | None = None) -> str:
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

# Silent-h words take "an" even though they start with a consonant.
SILENT_H = {"hour", "honest", "heir", "herb", "honor", "honour", "hours", "honesty"}

# "u" words pronounced /juː/ take "a" despite the vowel letter.
YOU_SOUND = ("user", "unique", "unit", "universe", "utility", "uniform", "unified")


def a_or_an(word: str) -> str:
    """Return the article a phrase takes, by pronunciation not spelling.

    The decision comes from the first word, so "honest answer" and
    "user account" work as well as their single-word forms.
    """
    first = word.split()[0] if word.split() else ""
    if not first:
        return "a"
    lower = first.lower()
    # Plurals of the silent-h set follow the same pronunciation.
    if lower in SILENT_H or (lower.endswith("s") and lower[:-1] in SILENT_H):
        return "an"
    # Capitalized /juː/ words (Unicode, European) follow the u-rule too.
    if lower.startswith(YOU_SOUND) or lower.startswith(("unicode", "european")):
        return "a"
    # Words beginning with a pronounced "w" sound are "a" despite "o".
    if lower.startswith(("one", "once")):
        return "a"
    return "an" if first[0] in VOWELS else "a"


def pluralize(word: str) -> str:
    """Naive pluralization for table names."""
    if word.endswith(("s", "x", "ch", "sh")):
        return word + "es"
    if word.endswith("y") and len(word) > 1 and word[-2] not in VOWELS:
        return word[:-1] + "ies"
    return word + "s"


def split_words(name: str) -> list[str]:
    """Split any naming style into words without separators."""
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    # acronym boundary: uppercase run followed by Upper+lower word
    spaced = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", spaced)
    spaced = re.sub(r"[(){}\[\]]", " ", spaced)
    return [w for w in spaced.replace("_", " ").replace("-", " ").split() if w]


def initials(name: str) -> str:
    """Abbreviate a name to initials, e.g. 'Total Sales' -> 'TS'."""
    return "".join(w[0].upper() for w in split_words(name))
