"""SARIF 2.1.0 documents for CI code scanning of DAX measures."""

from __future__ import annotations

from typing import Any

from . import __version__
from .lint import RULES

REPO_URL = "https://github.com/SourinRakshit-ai/aibi-toolkit"


def _escape(part: str) -> str:
    return part.replace("~", "~0").replace("/", "~1")


def build_sarif(
    findings: list[tuple[str, str, str, str]], model_path: str
) -> dict[str, Any]:
    """One-run SARIF 2.1.0 document for `aibi lint --sarif`.

    Each finding is (table, measure, rule id, message). A JSON
    Pointer fragment points at the measure in the model file's real
    `tables[].measures[]` shape, with RFC 6901 escaping on name parts.
    """
    results: list[dict[str, Any]] = []
    for table, measure, rule_id, message in findings:
        pointer = f"#/tables/{_escape(table)}/measures/{_escape(measure)}"
        results.append(
            {
                "ruleId": rule_id,
                "level": "warning",
                "message": {"text": message},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": f"{model_path}{pointer}"}
                        }
                    }
                ],
            }
        )
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "aibi-toolkit",
                        "version": __version__,
                        "informationUri": REPO_URL,
                        "rules": [
                            {
                                "id": rule.name,
                                "shortDescription": {"text": rule.message},
                            }
                            for rule in RULES
                        ],
                    }
                },
                "results": results,
            }
        ],
    }
