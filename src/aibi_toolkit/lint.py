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
    return findings


def lint_model(model: dict) -> dict:
    """Lint every measure in the model, grouped by measure name."""
    from .metadata import list_measures
    out: dict[str, list[str]] = {}
    for m in list_measures(model):
        findings = lint_dax(m.get("expression", ""))
        if findings:
            out[m["name"]] = findings
    return out
