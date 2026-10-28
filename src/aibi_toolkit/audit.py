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


def audit_score(model: dict) -> int:
    """Score 0-100 based on measure hygiene findings."""
    measures = list_measures(model)
    if not measures:
        return 100
    findings = audit_measures(model)
    problems = sum(len(v) for v in findings.values())
    return max(0, 100 - round(100 * problems / (2 * len(measures))))


def audit_tables(model: dict) -> dict:
    """Table-level findings: name issues and empty tables."""
    out: dict[str, list[str]] = {"empty": [], "bad_names": []}
    for t in model.get("tables", []):
        if not t.get("columns") and not t.get("measures"):
            out["empty"].append(t["name"])
        if t["name"] != t["name"].strip() or "  " in t["name"]:
            out["bad_names"].append(t["name"])
    return out
