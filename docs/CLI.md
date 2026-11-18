# CLI reference

Every command takes a model path first — a shared-schema JSON dump, or a
TMDL folder (`.pbip` project root, `*.Dataset` folder, or the
`definition/` directory). Output-oriented commands (`export`, `report`,
`synth`) take a destination path second.

## Exit codes

- `0` — the command ran and found nothing wrong (or produced its output).
- `1` — findings exist (`audit`, `lint`, `profile --json` when non-empty).
- `2` — usage error. A missing path, not valid JSON, or a top-level shape
  other than a JSON object prints a one-line reason on stderr — never a
  traceback.

Every `aibi` command supports `--help`.
