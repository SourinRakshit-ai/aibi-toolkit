from __future__ import annotations

from .metadata import Model

"""Static checks for DAX expressions and measure definitions."""

import re

BAD_FUNCTIONS = {
    "ALLSELECTED()": "no-argument ALLSELECTED is ambiguous in visuals",
    "CALCULATE([])": "empty CALCULATE filter",
}

def lint_dax(expression: str) -> list[str]:
    """Return lint findings for a single DAX expression."""
    findings = []
    if "/" in expression and re.search(r"(?i)\bDIVIDE\s*\(", expression) is None:
        findings.append("use DIVIDE instead of / to guard divide-by-zero")
    for token, reason in BAD_FUNCTIONS.items():
        if token in expression:
            findings.append(reason)
    if re.search(r"(?i)\bIFERROR\b", expression):
        findings.append("IFERROR hides real errors; handle specific cases")
    if re.search(r"(?i)\bCOUNTROWS\s*\(\s*VALUES\s*\(", expression):
        findings.append("COUNTROWS(VALUES(x)) is DISTINCTCOUNT(x) — shorter and faster")
    if re.search(r"(?i)\bIF\s*\(\s*TRUE\s*\(\s*\)\s*,", expression):
        findings.append("IF(TRUE(), x, y) is always x — the condition never branches")
    if re.search(r"(?i)\bIF\s*\(\s*FALSE\s*\(\s*\)\s*,", expression):
        findings.append("IF(FALSE(), x, y) is always y — the condition never branches")
    if re.search(r"(?:\bNOT\s*\(|!)\s*(?:\bNOT\s*\(|!)", expression, re.IGNORECASE):
        findings.append("NOT(NOT(x)) is just x — drop the double wrapper")
    return findings

def lint_model(model: Model) -> dict[str, list[str]]:
    """Lint every measure in the model, grouped by measure name."""
    from .metadata import list_measures
    out: dict[str, list[str]] = {}
    for m in list_measures(model):
        findings = lint_dax(m.get("expression", ""))
        if findings:
            out[m["name"]] = findings
    return out
