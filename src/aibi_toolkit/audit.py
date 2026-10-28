"""Model hygiene audits for semantic models."""

from .metadata import list_measures, model_summary


def audit_measures(model: dict) -> dict:
    """Run a measure hygiene audit and return findings by category."""
    measures = list_measures(model)
    findings: dict[str, list[str]] = {
        "missing_format": [],
        "duplicate_names": [],
        "long_names": [],
    }
    seen: set[str] = set()
    for m in measures:
        if not m.get("formatString"):
            findings["missing_format"].append(m["name"])
        if m["name"].lower() in seen:
            findings["duplicate_names"].append(m["name"])
        seen.add(m["name"].lower())
        if len(m["name"]) > 64:
            findings["long_names"].append(m["name"])
    return findings
