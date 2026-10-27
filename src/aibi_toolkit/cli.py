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
