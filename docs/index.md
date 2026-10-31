# aibi-toolkit

CLI + library for cleaning up Power BI / Tableau semantic-model metadata.

```bash
pip install .
aibi --help
```

| Command  | Purpose                          |
| -------- | -------------------------------- |
| summary  | object counts                    |
| audit    | hygiene findings + score         |
| lint     | DAX rule findings                |
| export   | measures to CSV                  |
| diagram  | mermaid ER diagram               |
| fix      | naming/format auto-fixes         |
| report   | markdown audit report            |
| synth    | demo model generator             |
