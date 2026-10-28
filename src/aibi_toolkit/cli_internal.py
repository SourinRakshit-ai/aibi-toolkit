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
