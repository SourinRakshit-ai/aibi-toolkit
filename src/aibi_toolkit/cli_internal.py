"""Internal CLI command implementations, split out for readability."""


import sys

from aibi_toolkit.metadata import Model


def _model(path: str) -> Model:
    """Load a model from disk or exit 2 with a one-line reason."""
    import json

    from .metadata import load_model
    try:
        return load_model(path)
    except FileNotFoundError:
        print(f"aibi: cannot read {path}: no such file or directory", file=sys.stderr)
        raise SystemExit(2)
    except json.JSONDecodeError as exc:
        print(f"aibi: {path}: not valid JSON ({exc})", file=sys.stderr)
        raise SystemExit(2)
    except (ValueError, TypeError) as exc:
        print(f"aibi: {path}: {exc}", file=sys.stderr)
        raise SystemExit(2)


def cmd_audit(model_path: str, json_out: bool = False) -> int:
    import json

    from aibi_toolkit.audit import audit_measures, audit_score
    model = _model(model_path)
    findings = audit_measures(model)
    if json_out:
        print(json.dumps({"score": audit_score(model), "findings": findings}, indent=2))
        return 1 if any(findings.values()) else 0
    for category, names in findings.items():
        for n in names:
            print(f"[{category}] {n}")
    print(f"score={audit_score(model)}")
    return 1 if any(findings.values()) else 0


def cmd_lint(model_path: str, json_out: bool = False) -> int:
    import json

    from aibi_toolkit.lint import lint_model
    findings = lint_model(_model(model_path))
    if json_out:
        print(json.dumps({"lint": findings}, indent=2))
        return 1 if findings else 0
    for name, issues in findings.items():
        for issue in issues:
            print(f"[lint] {name}: {issue}")
    return 1 if findings else 0


def cmd_export(model_path: str, out_path: str) -> int:
    from aibi_toolkit.csvio import export_measures
    from aibi_toolkit.metadata import list_measures
    try:
        n = export_measures(list_measures(_model(model_path)), out_path)
    except OSError as exc:
        print(f"aibi: cannot write {out_path}: {exc.strerror or exc}", file=sys.stderr)
        return 2
    print(f"exported {n} measures to {out_path}")
    return 0


def cmd_diagram(model_path: str) -> int:
    from aibi_toolkit.diagram import mermaid_er
    print(mermaid_er(_model(model_path)))
    return 0


def cmd_fix(model_path: str, dry_run: bool = False) -> int:
    import json

    from aibi_toolkit.autofix import autofix_model

    model = _model(model_path)
    result = autofix_model(model)
    for c in result["changes"]:
        print(f"fixed: {c}")
    if not dry_run and result["count"]:
        print(json.dumps(model, indent=2))
    return 0 if result["count"] else 1


def cmd_report(model_path: str, out_path: str) -> int:
    from aibi_toolkit.report import write_report
    try:
        write_report(_model(model_path), out_path)
    except OSError as exc:
        print(f"aibi: cannot write {out_path}: {exc.strerror or exc}", file=sys.stderr)
        return 2
    print(f"report written to {out_path}")
    return 0


def cmd_synth(out_path: str, tables: int = 3) -> int:
    import json

    from aibi_toolkit.sample import sample_model
    model = sample_model(tables=tables)
    from pathlib import Path
    try:
        Path(out_path).write_text(json.dumps(model, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"aibi: cannot write {out_path}: {exc.strerror or exc}", file=sys.stderr)
        return 2
    print(f"sample model written to {out_path}")
    return 0


def cmd_profile(model_path: str, json_out: bool = False) -> int:
    import json

    from aibi_toolkit.profile import profile_model
    p = profile_model(_model(model_path))
    if json_out:
        print(json.dumps(p, indent=2))
        return 0
    print(f"count={p['count']} avg={p['avg']} max={p['max']}")
    for name in p["heavy"]:
        print(f"[heavy] {name}")
    return 0
