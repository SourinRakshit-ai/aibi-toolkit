# Auditing

```bash
aibi audit model.json
```

Exits non-zero when findings exist, so it works as a CI gate:

```yaml
- run: aibi audit model.json
```

## Score

The 0-100 score penalizes missing formats (heaviest), duplicate names,
and overly long names.

## Relationship checks

`integrity.check_relationships` flags inactive and bidirectional
relationships; `check_cardinality` flags missing cardinality.
