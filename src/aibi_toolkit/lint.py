"""Static checks for DAX expressions and measure definitions.

Rules are a data catalog: each has a stable name, a regex pattern and a
message with the concrete rewrite. `lint_dax` projects the catalog into
message strings; `lint_findings` keeps rule attribution for tooling.
"""

from __future__ import annotations

import re
from typing import NamedTuple

from .metadata import Model


class Rule(NamedTuple):
    name: str
    pattern: str
    message: str


RULES: tuple[Rule, ...] = (
    Rule(
        "raw_division",
        r"(?!)",  # handled specially: a slash with no DIVIDE anywhere
        "use DIVIDE instead of / to guard divide-by-zero",
    ),
    Rule(
        "allselected_no_args",
        r"ALLSELECTED\(\)",
        "no-argument ALLSELECTED is ambiguous in visuals",
    ),
    Rule(
        "empty_calculate_filter",
        r"CALCULATE\(\[\]\)",
        "empty CALCULATE filter",
    ),
    Rule("iferror", r"\bIFERROR\b", "IFERROR hides real errors; handle specific cases"),
    Rule(
        "countrows_values",
        r"\bCOUNTROWS\s*\(\s*VALUES\s*\(",
        "COUNTROWS(VALUES(x)) is DISTINCTCOUNT(x) — shorter and faster",
    ),
    Rule(
        "if_true_branch",
        r"\bIF\s*\(\s*TRUE\s*\(\s*\)\s*,",
        "IF(TRUE(), x, y) is always x — the condition never branches",
    ),
    Rule(
        "if_false_branch",
        r"\bIF\s*\(\s*FALSE\s*\(\s*\)\s*,",
        "IF(FALSE(), x, y) is always y — the condition never branches",
    ),
    Rule(
        "double_negation",
        r"(?:\bNOT\s*\(|!)\s*(?:\bNOT\s*\(|!)",
        "NOT(NOT(x)) is just x — drop the double wrapper",
    ),
    Rule(
        "nested_trim",
        r"\bTRIM\s*\(\s*TRIM\s*\(",
        "TRIM(TRIM(x)) is just TRIM(x) — one call trims everything the pair can",
    ),
    Rule(
        "nested_upper",
        r"\bUPPER\s*\(\s*UPPER\s*\(",
        "UPPER(UPPER(x)) is just UPPER(x) — UPPER is idempotent",
    ),
    Rule(
        "nested_lower",
        r"\bLOWER\s*\(\s*LOWER\s*\(",
        "LOWER(LOWER(x)) is just LOWER(x) — LOWER is idempotent",
    ),
    Rule(
        "nested_abs",
        r"\bABS\s*\(\s*ABS\s*\(",
        "ABS(ABS(x)) is just ABS(x) — ABS is idempotent",
    ),
    Rule(
        "nested_int",
        r"\bINT\s*\(\s*INT\s*\(",
        "INT(INT(x)) is just INT(x) — INT is idempotent",
    ),
    Rule(
        "distinctcount_values",
        r"\bDISTINCTCOUNT\s*\(\s*VALUES\s*\(",
        "DISTINCTCOUNT(VALUES(x)) is DISTINCTCOUNT(x) — one distinct pass",
    ),
    Rule(
        "true_comparison",
        r"=\s*TRUE\s*\(\s*\)",
        "[flag] = TRUE() is [flag] — the column is already the boolean",
    ),
    Rule(
        "false_comparison",
        r"=\s*FALSE\s*\(\s*\)",
        "[flag] = FALSE() is NOT [flag] — invert the column instead",
    ),
    Rule(
        "abs_impossible",
        r"\bABS\s*\([^()]*\)\s*<\s*0\b|\b0\s*>\s*ABS\s*\([^()]*\)",
        "ABS(x) < 0 can never hold — check the sign or drop the condition",
    ),
    Rule(
        "countrows_zero",
        r"\bCOUNTROWS\s*\([^()]*\)\s*=\s*0\b|\b0\s*=\s*COUNTROWS\s*\([^()]*\)",
        "COUNTROWS(t) = 0 is ISEMPTY(t) — one call says the same thing",
    ),
    Rule(
        "blank_equality",
        r"=\s*BLANK\s*\(\s*\)",
        "[x] = BLANK() compares against BLANK instead of asking ISBLANK(x)",
    ),
    Rule(
        "blank_inequality",
        r"<>\s*BLANK\s*\(\s*\)",
        "[x] <> BLANK() compares against BLANK instead of NOT(ISBLANK(x))",
    ),
)

_COMPILED: tuple[tuple[Rule, re.Pattern[str]], ...] = tuple(
    (rule, re.compile(rule.pattern, re.IGNORECASE)) for rule in RULES
)


def lint_findings(expression: str) -> list[tuple[str, str]]:
    """All findings as (rule name, message) pairs, in catalog order."""
    findings: list[tuple[str, str]] = []
    for rule, compiled in _COMPILED:
        if rule.name == "raw_division":
            if "/" in expression and not re.search(r"(?i)\bDIVIDE\s*\(", expression):
                findings.append((rule.name, rule.message))
        elif compiled.search(expression):
            findings.append((rule.name, rule.message))
    return findings


def lint_dax(expression: str) -> list[str]:
    """Return lint findings for a single DAX expression."""
    return [message for _, message in lint_findings(expression)]


def lint_model_findings(model: Model) -> list[tuple[str, str, str]]:
    """Per-measure findings as (measure name, rule, message) triples."""
    from .metadata import list_measures
    out: list[tuple[str, str, str]] = []
    for m in list_measures(model):
        for rule, message in lint_findings(m.get("expression", "")):
            out.append((m["name"], rule, message))
    return out


def lint_model(model: Model) -> dict[str, list[str]]:
    """Lint every measure in the model, grouped by measure name."""
    out: dict[str, list[str]] = {}
    for name, _, message in lint_model_findings(model):
        out.setdefault(name, []).append(message)
    return out
