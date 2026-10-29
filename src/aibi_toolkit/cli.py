"""Command-line interface for aibi-toolkit."""

import argparse


COMMANDS = (
    ("summary", "Print model summary counts"),
    ("tables", "List tables in a model"),
    ("audit", "Run measure hygiene audit"),
    ("lint", "Lint DAX expressions"),
    ("export", "Export measures to CSV"),
)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aibi", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd, help_text in COMMANDS:
        s = sub.add_parser(cmd, help=help_text)
        s.add_argument("model")
        if cmd == "export":
            s.add_argument("out")
    args = parser.parse_args(argv)
    return _dispatch(args)


def _dispatch(args) -> int:
    from . import cli_internal
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
        return cli_internal.cmd_audit(args.model)
    if args.command == "lint":
        return cli_internal.cmd_lint(args.model)
    if args.command == "export":
        return cli_internal.cmd_export(args.model, args.out)
    return 0
