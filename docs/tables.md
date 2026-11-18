# Listing tables

`aibi tables` prints one table name per line — useful for a quick sanity
check on what the model actually contains before an audit:

```bash
$ aibi tables model.json
Sales
Customer
Product
Date
```

If a model has been edited outside the app, `tables` is the first thing to
run to see what survived the round trip.

## Interpreting the output

- **Tables** come from `model.get("tables")`, in the raw order the dump
  stores them.
- Empty tables are not listed separately by this command; `aibi audit`
  reports those separately in its table-level findings.
- Names print exactly as they appear in the model, including any stray
  whitespace an app may have written. That is intentional — it makes
  the output a reliable check for hand-edited files.

## Common follow-ups

- Feed the output into a diff: `aibi tables before.json > tables-before.txt` — it shows exactly what disappeared in an edit.
- Run `aibi audit` next for the hygiene checks, or `aibi diagram` to see how the tables relate.
