# aibi-toolkit

Small, dependency-light Python helpers for cleaning up Power BI / Tableau
semantic-model metadata: naming conventions, measure format strings, DAX
snippets, and CSV round-tripping.

Status: v0.2 — stable API for naming and format helpers.

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
