# aibi-toolkit

CLI + library for cleaning up Power BI / Tableau semantic-model metadata.

```bash
pip install aibi-toolkit
aibi --help
```

| Command  | Purpose                          |
| -------- | -------------------------------- |
| summary  | object counts                    |
| tables   | list table names                 |
| audit    | hygiene findings + score         |
| lint     | DAX rule findings                |
| export   | measures to CSV                  |
| diagram  | mermaid ER diagram               |
| fix      | naming/format auto-fixes         |
| report   | markdown audit report            |
| synth    | demo model generator             |

## Using the toolkit

Start with the [quick audit example](https://github.com/SourinRakshit-ai/aibi-toolkit/tree/main/examples#readme)
in the repo, or dive into the pages below for each command family:

- [Input formats](input.md) — JSON dumps vs `.pbip` TMDL folders
- [Naming](naming.md) and [format strings](format-strings.md)
- [Auditing](audit.md) and [linting](lint.md)
- [Tables](tables.md) for the table listing and follow-ups
- [Autofixes](autofix.md) and [profiling](profiling.md)
- [Diagrams](diagram.md) and the [CLI reference](CLI.md)

New in v0.8: `aibi profile` for expression complexity, role-playing
dimension detection, and word/naming utilities.
