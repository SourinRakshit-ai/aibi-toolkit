# Profiling

```bash
aibi profile model.json
```

Every `CALCULATE`, `FILTER`, `VAR` and `RETURN` adds weight. Weights of 5+
are flagged as heavy candidates for analysis.

## Tiers

| Weight | Tier    |
| ------ | ------- |
| 0-2    | light   |
| 3-5    | medium  |
| 6+     | heavy   |
