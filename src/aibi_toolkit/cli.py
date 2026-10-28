"""Command-line interface for aibi-toolkit."""

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aibi", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd, help_text in (
        ("summary", "Print model summary counts"),
        ("tables", "List tables in a model"),
        ("audit", "Run measure hygiene audit"),
    ):
        s = sub.add_parser(cmd, help=help_text)
        s.add_argument("model")
    args = parser.parse_args(argv)

    if args.command == "summary":
        from aibi_toolkit.metadata import load_model, model_summary
        s = model_summary(load_model(args.model))
        print(f"tables={s['tables']} measures={s['measures']} columns={s['columns']}")
        return 0
    if args.command == "tables":
        from aibi_toolkit.metadata import load_model, list_tables
        for t in list_tables(load_model(args.model)):
            print(t)
        return 0
    if args.command == "audit":
        from aibi_toolkit.cli_internal import cmd_audit
        return cmd_audit(args.model)
    return 0
