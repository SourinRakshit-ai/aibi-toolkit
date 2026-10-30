# aibi-toolkit

Small, dependency-light Python helpers for cleaning up Power BI / Tableau
semantic-model metadata: naming conventions, measure format strings, DAX
snippets, and CSV round-tripping.

Status: v0.6 — autofix, mermaid diagrams and integrity checks. See [CHANGELOG](CHANGELOG.md).

## Install

```bash
pip install .
```

## CLI usage

```bash
aibi summary path/to/model.json
```

## Modules

| Module      | Purpose                                  |
| ----------- | ---------------------------------------- |
| `naming`    | snake_case / display-name normalization  |
| `measure`   | format-string builders and detection     |
| `dax`       | common DAX measure snippets              |
| `metadata`  | model JSON inspection and summaries      |
| `csvio`     | CSV export/import of measure inventories |

## Testing

```bash
make test
```

## Python usage

```python
from aibi_toolkit.naming import to_display_name
to_display_name("total_sales_amount")  # -> 'Total Sales Amount'
```

## Format helpers

```python
from aibi_toolkit.measure import currency_format
currency_format("EUR", 0)  # -> '€#,0'
```

## CLI commands

```bash
aibi summary model.json   # table/measure/column counts
aibi tables model.json    # list table names
```

## Auditing

```bash
aibi audit model.json   # hygiene findings + 0-100 score, non-zero exit on findings
```

## Linting

```bash
aibi lint model.json
```

## All CLI commands

```bash
aibi summary model.json
aibi tables model.json
aibi audit model.json
aibi lint model.json
aibi export model.json out.csv
```

## Diagrams and auto-fixes

```bash
aibi diagram model.json       # mermaid ER diagram for the model
aibi fix --dry-run model.json # preview naming/format fixes
```
