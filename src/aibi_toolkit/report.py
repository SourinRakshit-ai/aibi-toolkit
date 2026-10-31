"""Generate a markdown audit report for a semantic model."""

from .audit import audit_measures, audit_tables, audit_score
from .integrity import check_relationships, orphan_tables, check_cardinality
from .tables import markdown_table


def generate_report(model: dict, title: str = "Model Audit Report") -> str:
    """Build a full markdown report string."""
    sections = [f"# {title}", ""]
    sections += _overview(model)
    sections += _measure_findings(model)
    sections += _table_findings(model)
    sections += _relationship_findings(model)
    return "\n".join(sections)


def _overview(model: dict) -> list[str]:
    from .metadata import model_summary
    s = model_summary(model)
    return [
        "## Overview",
        "",
        f"Score: **{audit_score(model)}/100**",
        "",
        f"- Tables: {s['tables']}",
        f"- Measures: {s['measures']}",
        f"- Columns: {s['columns']}",
        "",
    ]


def _measure_findings(model: dict) -> list[str]:
    f = audit_measures(model)
    rows = [{"category": k, "count": len(v), "examples": ", ".join(v[:3])} for k, v in f.items() if v]
    out = ["## Measure findings", ""]
    out += (markdown_table(rows, columns=["category", "count", "examples"]).splitlines() if rows else ["No measure findings."])
    return out + [""]


def _table_findings(model: dict) -> list[str]:
    f = audit_tables(model)
    orphans = orphan_tables(model)
    out = ["## Table findings", ""]
    if f["empty"]:
        out += [f"- Empty tables ({len(f['empty'])}): {', '.join(f['empty'][:5])}"]
    if f["bad_names"]:
        out += [f"- Bad table names: {', '.join(f['bad_names'][:5])}"]
    if orphans:
        out += [f"- Orphan tables: {', '.join(orphans[:5])}"]
    if not out[2:]:
        out += ["No table findings."]
    return out + [""]


def _relationship_findings(model: dict) -> list[str]:
    r = check_relationships(model)
    missing = check_cardinality(model)
    out = ["## Relationship findings", "", f"- Inactive relationships: {len(r['inactive'])}",
           f"- Bidirectional filters: {len(r['bidirectional'])}",
           f"- Missing cardinality: {len(missing)}", ""]
    return out
