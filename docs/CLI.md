# CLI reference

Every command takes a model path first. A model path may be either:

- a shared-schema JSON dump (`model.json` produced by your model tool), or
- a `.pbip`-style TMDL directory — a project root, a `*.Dataset` folder, or
  a bare `definition/` directory. `definition/tables/*.tmdl` feeds the table
  list; `definition/relationships.tmdl` feeds the relationship checks.

Output-oriented commands (`export`, `report`, `lint`, `fix`, `profile`,
`summary`, `tables`, `audit`, `diagram`) are described here. `synth`
generates a sample model instead of reading one.

## Summary

```bash
$ aibi summary model.json
tables=4 measures=8 columns=4

$ aibi summary model.json --json
{"tables": 4, "measures": 8, "columns": 4}
```

Prints one line: `tables=N measures=N columns=N`. `tables` counts table
objects; `measures` counts measure objects; `columns` counts columns in
table objects. `--json` prints the same data as
`{"tables": 4, "measures": 8, "columns": 4}`.

### Exit codes

- `0` — model loaded, line printed.
- `2` — model path missing, non-JSON, or top-level shape not an object.

## Tables

```bash
$ aibi tables model.json
Sales
Customer
Product
Date

$ aibi tables model.json --json
["Sales", "Customer", "Product", "Date"]
```

One table name per line, in persisted order. `--json` prints
`["Sales", "Customer", "Product", "Date"]` (a JSON array, in the same order).

### Exit codes

- `0` — model loaded, list printed.
- `2` — model path missing, non-JSON, or top-level shape not an object.

## Audit

```bash
$ aibi audit model.json
[missing_format] Measure 1
[duplicate_names] Measure 1
score=38
```

Findings are `[category] measure name`, one per line, then `score=N/100` at
the bottom. Categories: `missing_format` (no `formatString`), `duplicate_names`
(case-insensitive duplicate measure names), `long_names` (over 64 chars).

`--json` prints `{"score": 38, "findings": {category: [names]}}` instead of
the text output — same content, easier to parse in CI.

### Exit codes

- `1` — at least one finding.
- `0` — model loaded and clean (score is not printed in that case; only
  `no findings` would appear, currently it does — check empty output).

## Lint

```bash
$ aibi lint model.json
[lint] Measure name: use DIVIDE instead of / to guard divide-by-zero
```

`aibi lint` is the DAX-oriented static check. Findings are `[lint] measure
name: <reason>`. No output means the sample passed every check — return code
is then `0`.

`--json` prints `{"lint": {measure_name: [reasons]}}` for machine reading.
`--list-rules` prints the rule inventory (name and rewrite message) and exits
0 without reading a model; `--list-rules --json` emits
`[{"name": ..., "message": ...}]`.

### Exit codes

- `1` — at least one finding.
- `0` — no findings.

## Fix

```bash
$ aibi fix model.json
fixed: measure 'Measure 1' -> 'Measure'
fixed: format for 'Measure' -> $#,0.00
```

Normalises what the audit would flag — names (snake_case/kebab/collapse),
format strings, extras in the dump. `--dry-run` prints each proposed fix
without touching anything.

### Exit codes

- `0` — fixes were proposed (or applied when `--dry-run` is omitted; same count).
- `1` — nothing to fix.
- `2` — model path missing.

## Profile

```bash
$ aibi profile model.json
count=8 avg=0.0 max=0
```

Expression-complexity profile. `count` / `avg` / `max` are counts of DAX
weight; heavier measures matter more in review. `--json` exposes `{"count":
N, "avg": N, "max": N, "heavy": [names]}` for tooling.

### Exit codes

- `0` — model loaded.
- `2` — model path missing.

## Export

```bash
$ aibi export model.json out.csv
exported 8 measures to out.csv
```

Writes CSV with columns `table,name,expression,formatString`. Unwrapped
measure rows carry their enclosing table in the left column.

### Exit codes

- `0` — CSV written.
- `2` — model path missing, or output path unwritable. One-line reason on
  stderr; never a traceback.

## Report

```bash
$ aibi report model.json out.md
report written to out.md
```

Markdown report: `# Model Audit Report`, score, tables/measures, measure
findings, table findings (empty tables, bad names), relationship findings
(inactive, bidirectional, missing cardinality), plus an appendix of rules.

### Exit codes

- `0` — report written.
- `2` — model path missing, or output path unwritable. One-line reason on
  stderr; never a traceback.

## Diagram

```bash
$ aibi diagram model.json
erDiagram
    Sales ||--o{ Customer : has
    Sales ||--o{ Product : has
```

Writes a mermaid `erDiagram` to stdout. Paste it into a mermaid-rendered
markdown document or view in the mermaid CLI.

### Exit codes

- `0` — diagram printed.
- `2` — model path missing.

## Synth

```bash
$ aibi synth out.json
sample model written to out.json
```

Writes a small `model.json` suitable as scaffolding, or as a feed for the
other commands. Tables seeded: `Sales`, `Customer`, `Product`, `Date` with
two measures each. `--tables N` overrides the table count.

### Exit codes

- `0` — file written.
- `2` — file path unwritable.

## Explain

```bash
$ aibi explain double_negation
double_negation
NOT(NOT(x)) is just x — drop the double wrapper
pattern: (?:\bNOT\s*\(|!)\s*(?:\bNOT\s*\(|!)
```

With no rule name, `aibi explain` prints the same inventory as
`--list-rules` and exits 0. `--json` prints `{"name", "pattern",
"message"}` for one rule, or an array for the inventory. Names are
case-insensitive; an unknown name exits 2 with the inventory on stderr.

### Exit codes

- `0` — rule found (or no name given).
- `2` — unknown rule name.

## Every command at a glance

| Command | Reads model | Writes | Exit codes |
| --- | --- | --- | --- |
| `summary` | yes | stdout | 0 / 2 |
| `tables` | yes | stdout | 0 / 2 |
| `audit` | yes | stdout | 0 / 1 / 2 |
| `lint` | yes | stdout | 0 / 1 / 2 |
| `fix` | yes | stdout / model | 0 / 1 / 2 |
| `profile` | yes | stdout | 0 / 2 |
| `diagram` | yes | stdout | 0 / 2 |
| `export` | yes | CSV | 0 / 2 |
| `report` | yes | markdown | 0 / 2 |
| `synth` | no | JSON | 0 / 2 |
| `explain` | no | stdout | 0 / 2 |

## Exit codes (global)

- `0` — the command produced its output (or clean run).
- `1` — findings exist on an audit/lint-style command.
- `2` — usage error. Missing path, non-JSON, wrong top-level shape, or an
  unwritable output path — always one line on stderr, never a traceback.

Every command supports `--help`.
