# aibi-toolkit examples

Runnable demos, no fixtures required — every script generates its own sample
model via `sample_model()`/`sample_csv()` so they work from a fresh checkout.

```bash
pip install .
python examples/quick_audit.py     # hygiene audit + score
python examples/csv_workflow.py    # export / diff inventories across two CSVs
python examples/er_diagram.py      # mermaid ER + table diagram rendering
python examples/tmdl_tour.py       # point aibi at a TMDL folder and audit it
```

For a deeper tour, the [docs](https://sourinrakshit-ai.github.io/aibi-toolkit/)
walk through each command.
