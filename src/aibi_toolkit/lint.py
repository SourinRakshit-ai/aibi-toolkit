"""Static checks for DAX expressions and measure definitions."""

import re

BAD_FUNCTIONS = {
    "ALLSELECTED()": "no-argument ALLSELECTED is ambiguous in visuals",
    "CALCULATE([])": "empty CALCULATE filter",
}


def lint_dax(expression: str) -> list[str]:
    """Return lint findings for a single DAX expression."""
    findings = []
    if re.search(r"(?i)\bDIVIDE\s*\(\s*[^\s,]+\s*,\s*[^\s,]+\s*\)", expression) is None \
            and re.search(r"(?i)\b/\s*", expression):
        findings.append("use DIVIDE instead of / to guard divide-by-zero")
    for token, reason in BAD_FUNCTIONS.items():
        if token in expression:
            findings.append(reason)
    if re.search(r"(?i)\bIFERROR\b", expression):
        findings.append("IFERROR hides real errors; handle specific cases")
    return findings
