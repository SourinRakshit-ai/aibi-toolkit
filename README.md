# aibi-toolkit

*aibi* — CLI + library for cleaning up Power BI / Tableau semantic-model
metadata. Companion to [aibi-dax](https://github.com/SourinRakshit-ai/aibi-dax):
where aibi-dax checks the DAX expressions inside your measures, aibi-toolkit
checks the model around them — naming conventions, format strings, duplicate
measures, empty tables, relationships, hygiene.

[![CI](https://github.com/SourinRakshit-ai/aibi-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/SourinRakshit-ai/aibi-toolkit/actions/workflows/ci.yml)
[![Lint](https://github.com/SourinRakshit-ai/aibi-toolkit/actions/workflows/lint.yml/badge.svg)](https://github.com/SourinRakshit-ai/aibi-toolkit/actions/workflows/lint.yml)
[![Python](https://img.shields.io/badge/python-3.10–3.13-blue)](pyproject.toml)
[![Types](https://img.shields.io/badge/mypy-strict-blue)](pyproject.toml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](.github/workflows/lint.yml)
[![Docs](https://img.shields.io/badge/docs-live-informational)](https://sourinrakshit-ai.github.io/aibi-toolkit/)
![License](https://img.shields.io/badge/license-MIT-green)

Runnable walkthroughs live in [`examples/`](examples/#readme).

## Why this exists

A semantic model is a shared asset, and it always drifts. Measure names pick
up stray spaces, missing format strings, duplicate definitions that nobody
deletes, and DAX smells that pass casual review. Nobody catches it, because
each file is small but the model is large, and nobody wants to be the one
recounting the measures by hand.

That is the failure mode aibi-toolkit was built for. It reads the dump, runs
the checks, gives you a score, and names the findings. The first pass
usually looks like: score 38, a dozen missing format strings, six duplicate
measures.

## What it does

- **`aibi audit`** — measure hygiene findings and a 0-100 score.
  Checks format strings, case-insensitive duplicate names, and measure
  name length. Exit 1 when anything is found, 0 when the model is clean,
  so a CI gate is one command.
- **`aibi lint`** — static checks on the DAX expressions: raw `/` without
  `DIVIDE`, no-argument `ALLSELECTED()`, `CALCULATE([])`, and `IFERROR`
  masking.
- **`aibi fix`** — applies naming and format-string fixes with `--dry-run`
  so you always see what would change before it changes.
- **`aibi summary`** — object counts; **`aibi tables`** — table list.
- **`aibi report`** — markdown audit report: score, finding counts,
  examples, for your own paper trail or a PR description.
- **`aibi diagram`** — mermaid ER diagram straight from the model.
- **`aibi profile`** — expression complexity: count, average, max weight,
  and the heaviest measures named.
- **`aibi synth`** — generate a sample model for trying the tool.
- **`aibi export`** — measures to CSV for external row-checks.

Full module map:

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

## Install

Not on PyPI yet; install from the repository. Issue [#5](https://github.com/SourinRakshit-ai/aibi-toolkit/issues/5) tracks the trusted-publishing release:

```bash
git clone https://github.com/SourinRakshit-ai/aibi-toolkit.git
cd aibi-toolkit
pip install .
aibi --help
```

## Quick start

Generate a sample model, then check it:

```bash
aibi synth model.json          # write a sample model
aibi summary model.json        # object counts
aibi audit model.json          # hygiene findings + 0-100 score
aibi lint model.json           # DAX rule findings
aibi audit model.json --json   # machine-readable output (also: lint, profile)
aibi report model.json out.md  # markdown audit report
aibi fix --dry-run model.json  # preview fixes before writing anything
```

Audit returns exit `1` when findings exist, `0` when clean, so a pipeline
that already has `set -e` fails immediately. Pass `--json` to `audit`,
`lint` or `profile` when you want a machine-readable result.

## How it helps

- **One number first.** The 0–100 score tells you whether the model
  deserves attention before you read a single measure. Score 38 usually
  means "regenerate formats and delete the dead duplicates"; score 92
  means "quick answer, move on".
- **Names and formats are the fix.** Around 90% of findings in real
  models are `missing_format` and duplicates after a bulk edit; both
  are auto-fixable by `aibi fix` with `--dry-run` for confirmation.
- **Exit codes mean CI.** `aibi audit model.json` returns 1 with any
  finding and 0 clean, so the release pipeline it belongs in fails where
  the merge should wait for you.
- **The report is the artifact.** `aibi report` gives a reviewer the
  score and a short list of examples, which is usually enough for the
  release meeting.

## What it is not

- **Not an aibi-dax substitute.** It lints DAX for narrowly-scoped
  patterns (raw `/`, no-arg `ALLSELECTED()`, `CALCULATE([])`, `IFERROR`
  hiding). For deep complexity scoring and anti-pattern detection,
  that is what [aibi-dax](https://github.com/SourinRakshit-ai/aibi-dax)
  is for.
- **Not a full TMDL/PBIP authoring tool.** It reads shared-schema
  model dumps; it does not write them back to disk yet
  (tracked in [#6](https://github.com/SourinRakshit-ai/aibi-toolkit/issues/6)).
- **Not a bug finder for DAX logic.** It checks static patterns; it
  cannot tell you your total is wrong. That still needs `EVALUATE`
  checks and your eyes.
- **Not a performance tool.** It has no cost model for queries; it
  flags patterns, not benchmarks.

## Commands

| Command | Purpose |
| ------- | ------- |
| `aibi summary model.json` | object counts |
| `aibi tables model.json` | list tables |
| `aibi audit model.json` | hygiene findings + 0-100 score |
| `aibi lint model.json` | DAX rule findings |
| `aibi fix --dry-run model.json` | preview naming/format fixes (omit `--dry-run` to apply) |
| `aibi profile model.json` | expression complexity: count, avg, max, heavy |
| `aibi diagram model.json` | mermaid ER diagram |
| `aibi export model.json out.csv` | measures to CSV |
| `aibi report model.json out.md` | markdown audit report |
| `aibi synth model.json` | generate a sample model |

## Docs and support

- **Docs site:** [sourinrakshit-ai.github.io/aibi-toolkit](https://sourinrakshit-ai.github.io/aibi-toolkit/) (`mkdocs gh-deploy`)
- **Issues:** [https://github.com/SourinRakshit-ai/aibi-toolkit/issues](https://github.com/SourinRakshit-ai/aibi-toolkit/issues)
- **Status:** `v1.2.0` on main. Not yet published to PyPI; trusted publishing
  for the repo is tracked in [#5](https://github.com/SourinRakshit-ai/aibi-toolkit/issues/5),
  with the pattern now proven by [aibi-dax](https://github.com/SourinRakshit-ai/aibi-dax).
- **Releases:** tagged `v*` triggers the `publish.yml` workflow once
  trusted publishing is configured.

## Development

```bash
make install        # pip install -e ".[dev]"
make test           # pytest -q
make typecheck      # mypy --strict src/aibi_toolkit/
make lint           # ruff check src/ tests/
make serve-docs     # mkdocs serve
```

MIT licensed. Roadmap lives in the issue tracker.
