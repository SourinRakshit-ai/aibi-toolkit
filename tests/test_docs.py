"""Docs smoke tests: the CLI examples in docs/CLI.md must match real output.

The docs are the public contract — drift fails release, not review.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DOCS = Path("docs/CLI.md")
CLI = [sys.executable, "-m", "aibi_toolkit"]


def test_every_fenced_aibi_command_parses() -> None:
    """Every `$ aibi ...` line in a ```bash fence must parse under `python -m aibi_toolkit`."""
    text = DOCS.read_text(encoding="utf-8")
    fences = re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
    assert fences, "docs/CLI.md has no ```bash fences"
    cmds = []
    for fence in fences:
        for line in fence.splitlines():
            if line.startswith("$ aibi "):
                cmds.append(line[len("$ aibi "):].strip())
    assert cmds, "docs/CLI.md exposes no aibi examples"
    for args in cmds:
        # model is a required first positional for every command
        argv = args.split()
        assert argv[0] in {"summary", "tables", "audit", "lint", "export", "report", "fix", "profile", "diagram", "synth"}, args


def test_cli_md_documents_every_command() -> None:
    """Every subcommand in the CLI must be documented in docs/CLI.md."""
    from aibi_toolkit.cli import COMMANDS

    text = DOCS.read_text(encoding="utf-8")
    for cmd, _ in COMMANDS:
        assert f"aibi {cmd}" in text, f"docs/CLI.md missing command: {cmd}"


def test_summary_json_fence_is_valid_json() -> None:
    """docs/CLI.md `summary --json` fence must parse as the printed dict."""
    text = DOCS.read_text(encoding="utf-8")
    match = re.search(r"\$ aibi summary model\.json --json\n(\{.*?\})\n```", text)
    assert match, "docs/CLI.md's summary --json fence drifted"
    payload = json.loads(match.group(1))
    assert set(payload) == {"tables", "measures", "columns"}
    assert all(isinstance(v, int) for v in payload.values())


def test_tables_json_fence_is_a_json_array_of_strings() -> None:
    """docs/CLI.md `tables --json` fence must parse as a JSON string array."""
    text = DOCS.read_text(encoding="utf-8")
    match = re.search(r"\$ aibi tables model\.json --json\n(\[.*?\])\n```", text)
    assert match, "docs/CLI.md's tables --json fence drifted"
    payload = json.loads(match.group(1))
    assert isinstance(payload, list)
    assert all(isinstance(x, str) for x in payload)
