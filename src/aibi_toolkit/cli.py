"""Command-line interface for aibi-toolkit."""

import argparse

COMMANDS = (
    ("summary", "Print model summary counts"),
    ("tables", "List tables in a model"),
    ("audit", "Run measure hygiene audit"),
    ("lint", "Lint DAX expressions"),
    ("diagram", "Print mermaid ER diagram"),
    ("fix", "Propose/apply naming and format fixes"),
    ("profile", "Expression complexity profile"),
    ("export", "Export measures to CSV"),
    ("report", "Write a markdown audit report"),
    ("synth", "Generate a sample model JSON"),
)

# Commands where args.model is an input and args.out is a write target.
WRITE_TARGETS = ("export", "report")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aibi", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd, help_text in COMMANDS:
        s = sub.add_parser(cmd, help=help_text)
        if cmd == "synth":
            s.add_argument("out")
            s.add_argument("--tables", type=int, default=3, help="number of tables in the sample model")
            continue
        s.add_argument("model")
        if cmd in WRITE_TARGETS:
            s.add_argument("out")
        if cmd == "fix":
            s.add_argument("--dry-run", action="store_true", help="print findings without applying")
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
    if args.command == "diagram":
        return cli_internal.cmd_diagram(args.model)
    if args.command == "fix":
        return cli_internal.cmd_fix(args.model, args.dry_run)
    if args.command == "report":
        return cli_internal.cmd_report(args.model, args.out)
    if args.command == "synth":
        return cli_internal.cmd_synth(args.out, args.tables)
    if args.command == "profile":
        return cli_internal.cmd_profile(args.model)
    return 0
