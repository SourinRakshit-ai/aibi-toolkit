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
    if re.search(r"\bTRIM\s*\(\s*TRIM\s*\(", expression, re.IGNORECASE):
        findings.append("TRIM(TRIM(x)) is just TRIM(x) — one call trims everything the pair can")
    if re.search(r"\bUPPER\s*\(\s*UPPER\s*\(", expression, re.IGNORECASE):
        findings.append("UPPER(UPPER(x)) is just UPPER(x) — UPPER is idempotent")
    if re.search(r"\bLOWER\s*\(\s*LOWER\s*\(", expression, re.IGNORECASE):
        findings.append("LOWER(LOWER(x)) is just LOWER(x) — LOWER is idempotent")
    if re.search(r"\bABS\s*\(\s*ABS\s*\(", expression, re.IGNORECASE):
        findings.append("ABS(ABS(x)) is just ABS(x) — ABS is idempotent")
    if re.search(r"\bINT\s*\(\s*INT\s*\(", expression, re.IGNORECASE):
        findings.append("INT(INT(x)) is just INT(x) — INT is idempotent")
    if re.search(r"\bDISTINCTCOUNT\s*\(\s*VALUES\s*\(", expression, re.IGNORECASE):
        findings.append("DISTINCTCOUNT(VALUES(x)) is DISTINCTCOUNT(x) — one distinct pass")
    if re.search(r"=\s*TRUE\s*\(\s*\)", expression, re.IGNORECASE):
        findings.append("[flag] = TRUE() is [flag] — the column is already the boolean")
    if re.search(r"=\s*FALSE\s*\(\s*\)", expression, re.IGNORECASE):
        findings.append("[flag] = FALSE() is NOT [flag] — invert the column instead")
    if re.search(r"\bABS\s*\([^()]*\)\s*<\s*0\b|\b0\s*>\s*ABS\s*\([^()]*\)", expression, re.IGNORECASE):
        findings.append("ABS(x) < 0 can never hold — check the sign or drop the condition")
    if re.search(r"\bCOUNTROWS\s*\([^()]*\)\s*=\s*0\b|\b0\s*=\s*COUNTROWS\s*\([^()]*\)", expression, re.IGNORECASE):
        findings.append("COUNTROWS(t) = 0 is ISEMPTY(t) — one call says the same thing")
    if re.search(r"=\s*BLANK\s*\(\s*\)", expression, re.IGNORECASE):
        findings.append("[x] = BLANK() compares against BLANK — ask ISBLANK(x) instead")
    if re.search(r"<>\s*BLANK\s*\(\s*\)", expression, re.IGNORECASE):
        findings.append("[x] <> BLANK() compares against BLANK — ask NOT(ISBLANK(x)) instead")
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
