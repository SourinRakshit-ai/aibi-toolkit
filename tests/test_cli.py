"""End-to-end tests driving the CLI parser and command dispatch."""

import json
from pathlib import Path

import pytest

from aibi_toolkit.cli import main
from aibi_toolkit.sample import sample_model


@pytest.fixture
def model_path(tmp_path):
    p = tmp_path / "model.json"
    p.write_text(json.dumps(sample_model(tables=3)), encoding="utf-8")
    return str(p)


def dispatch_argv(cmd, model_path, *extra):
    return main([cmd, model_path, *extra])


def test_summary_and_tables(model_path, capsys):
    assert dispatch_argv("summary", model_path) == 0
    assert "tables=3" in capsys.readouterr().out
    assert dispatch_argv("tables", model_path) == 0
    assert "Sales" in capsys.readouterr().out


def test_report_writes_markdown(model_path, tmp_path):
    out = tmp_path / "report.md"
    assert dispatch_argv("report", model_path, str(out)) == 0
    assert out.exists()


def test_synth_writes_model_json(tmp_path):
    out = tmp_path / "demo.json"
    assert main(["synth", str(out), "--tables", "2"]) == 0
    loaded = json.loads(out.read_text())
    assert len(loaded["tables"]) == 2


def test_export_csv(model_path, tmp_path):
    out = tmp_path / "measures.csv"
    assert dispatch_argv("export", model_path, str(out)) == 0
    assert out.exists()


def test_fix_dry_run_flag_parses(model_path, capsys):
    assert dispatch_argv("fix", model_path, "--dry-run") == 0
    assert "fixed:" in capsys.readouterr().out


def test_audit_and_lint_exit_cleanly(model_path):
    assert dispatch_argv("audit", model_path) in (0, 1)
    assert dispatch_argv("lint", model_path) in (0, 1)


def test_version_flag(capsys):
    import pytest as _pytest
    from aibi_toolkit.cli import main as _main
    with _pytest.raises(SystemExit) as e:
        _main(["--version"])
    assert e.value.code == 0
    assert "aibi-toolkit" in capsys.readouterr().out
