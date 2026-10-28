"""Command-line interface for aibi-toolkit."""

import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aibi", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    summary = sub.add_parser("summary", help="Print model summary counts")
    summary.add_argument("model")
    tables = sub.add_parser("tables", help="List tables in a model")
    tables.add_argument("model")
    args = parser.parse_args(argv)

    if args.command == "summary":
        from aibi_toolkit.metadata import load_model, model_summary
        s = model_summary(load_model(args.model))
        print(f"tables={s['tables']} measures={s['measures']} columns={s['columns']}")
    elif args.command == "tables":
        from aibi_toolkit.metadata import load_model, list_tables
        for t in list_tables(load_model(args.model)):
            print(t)
    return 0


def _cmd_audit(model_path: str) -> int:
    from aibi_toolkit.metadata import load_model
    from aibi_toolkit.audit import audit_measures, audit_score
    model = load_model(model_path)
    findings = audit_measures(model)
    for category, names in findings.items():
        for n in names:
            print(f"[{category}] {n}")
    print(f"score={audit_score(model)}")
    return 1 if any(findings.values()) else 0
