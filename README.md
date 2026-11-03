# aibi-toolkit

CLI + library for cleaning up Power BI / Tableau semantic-model metadata:
naming conventions, format strings, DAX snippets, hygiene auditing, linting,
relationship integrity, mermaid diagrams, and markdown audit reports.

[![CI](https://github.com/SourinRakshit-ai/aibi-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/SourinRakshit-ai/aibi-toolkit/actions/workflows/ci.yml)
[![Lint](https://github.com/SourinRakshit-ai/aibi-toolkit/actions/workflows/lint.yml/badge.svg)](https://github.com/SourinRakshit-ai/aibi-toolkit/actions/workflows/lint.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Install

```bash
pip install .
```

## Quick start

```bash
aibi summary model.json    # object counts
aibi audit model.json      # hygiene findings + 0-100 score
aibi lint model.json       # DAX rule findings
aibi report model.json out.md  # markdown audit report
aibi fix --dry-run model.json  # preview naming/format fixes
```

See the [docs index](docs/index.md) for the full command list.

## Framework coverage

| Area               | Module          |
| ------------------ | --------------- |
| Naming             | `naming`        |
| Format strings     | `measure`       |
| DAX snippets       | `dax`, `filters`|
| Model inspection   | `metadata`      |
| Auditing + linting | `audit`, `lint` |
| Integrity          | `integrity`     |
| Autofixes          | `autofix`       |
| Diagrams           | `diagram`       |
| Reports            | `report`        |
| Demo data          | `sample`        |
| Renderers          | `tables`        |
| Configuration      | `config`        |
| Profiling          | `profile`       |
| CSV round-trip     | `csvio`         |
