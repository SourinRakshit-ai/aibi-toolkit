# Changelog

## 1.0.2 - 2026-11-04
- Fixed: report/synth output-path parsing, missing --dry-run flag
  registration, and four duplicated COMMANDS/_dispatch blocks in cli.py.
- Added: end-to-end CLI tests (76 passing).

## 1.0.1 - 2026-11-04
- Fixed: CI on Python 3.10 — `tomllib` requires 3.11, so the config module
  now ships a minimal fallback parser behind a guarded import.
- Tests: 70 passing.

## 1.0.0 - 2026-11-03
- Release: API frozen. Postponed annotations across all modules, bare-pytest
  dev experience, README with badges and coverage table.

## 0.8.0 - 2026-11-02
- Added: profile module (expression weights, tiers, top-5 rankings),
  role-playing dimension detection, split_words/initials naming helpers,
  CLI profile command, PR auto-labeler workflow.

## 0.7.0 - 2026-11-01
- Added: report module (markdown audit report), sample module
  (deterministic demo models and CSVs), format validation + clamping,
  CLI report/synth commands, mkdocs docs site with strict build CI.

## 0.6.0 - 2026-10-31
- Added: autofix module (name + format fixes with change log), diagram
  module (mermaid ER + table graphs), orphan-table detection, terminal
  table renderer, CLI diagram/fix commands, starter config generator.

## 0.5.0 - 2026-10-30
- Added: lint module (DIVIDE/IFERROR rules), integrity module (inactive,
  bidirectional, cardinality checks), human-readable number scaling,
  format category keys, article/pluralize helpers, CLI lint and export
  commands, nightly build workflow.

## 0.4.0 - 2026-10-29
- Added: audit module (findings + score), config module (TOML + validation),
  kebab_case, strip_numbers, QTD/DATEADD snippets, audit CLI command,
  hidden-object and calculated-column inventories.


## 0.1.0 - 2026-10-27
- Initial release: naming, measure, dax, metadata, csvio modules + CLI.

## 0.2.0 - 2026-10-27
- Added: dedupe_names, truncate_name, normalize_all, MoM and RANKX snippets,
  date format presets, unused-measure detection, CSV summary stats.
