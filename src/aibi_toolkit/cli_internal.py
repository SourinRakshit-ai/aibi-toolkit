"""Internal CLI command implementations, split out for readability."""


def cmd_audit(model_path: str) -> int:
    from aibi_toolkit.metadata import load_model
    from aibi_toolkit.audit import audit_measures, audit_score
    model = load_model(model_path)
    findings = audit_measures(model)
    for category, names in findings.items():
        for n in names:
            print(f"[{category}] {n}")
    print(f"score={audit_score(model)}")
    return 1 if any(findings.values()) else 0


def cmd_lint(model_path: str) -> int:
    from aibi_toolkit.metadata import load_model
    from aibi_toolkit.lint import lint_model
    findings = lint_model(load_model(model_path))
    for name, issues in findings.items():
        for issue in issues:
            print(f"[lint] {name}: {issue}")
    return 1 if findings else 0


def cmd_export(model_path: str, out_path: str) -> int:
    from aibi_toolkit.metadata import load_model, list_measures
    from aibi_toolkit.csvio import export_measures
    n = export_measures(list_measures(load_model(model_path)), out_path)
    print(f"exported {n} measures to {out_path}")
    return 0
