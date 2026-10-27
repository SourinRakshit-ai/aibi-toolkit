"""Command-line interface for aibi-toolkit."""

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aibi", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    summary = sub.add_parser("summary", help="Print model summary counts")
    summary.add_argument("model", help="Path to model JSON dump")
    args = parser.parse_args(argv)

    if args.command == "summary":
        from aibi_toolkit.metadata import load_model, model_summary
        s = model_summary(load_model(args.model))
        print(f"tables={s['tables']} measures={s['measures']} columns={s['columns']}")


@staticmethod
def _banner(text: str) -> str:
    return f"=== {text} ==="
