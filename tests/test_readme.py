"""Smoke tests for the README quick-start block.

Parses every `aibi ...` command documented in the README and runs each one
against a generated sample model, so the docs can never drift from the CLI.
"""

import json
import shlex
from pathlib import Path

import pytest

from aibi_toolkit.cli import main
from aibi_toolkit.sample import sample_model

README = Path(__file__).resolve().parents[1] / "README.md"


def _quick_start_commands():
    text = README.read_text(encoding="utf-8")
    block = text.split("## Quick start", 1)[1].split("```bash", 1)[1].split("```", 1)[0]
    for line in block.splitlines():
        line = line.split("#", 1)[0].strip()
        if line.startswith("aibi "):
            yield shlex.split(line)[1:]


@pytest.mark.parametrize("argv", [list(a) for a in _quick_start_commands()])
def test_readme_quick_start(argv, tmp_path, capsys, monkeypatch):
    model = tmp_path / "model.json"
    model.write_text(json.dumps(sample_model(tables=2)), encoding="utf-8")
    argv = [str(model) if a == "model.json" else a for a in argv]
    # Run from tmp_path so output paths like out.md never land in the repo root.
    monkeypatch.chdir(tmp_path)
    rc = main(argv)
    assert rc in (0, 1)
    output = capsys.readouterr().out
    assert output.strip() or rc == 0