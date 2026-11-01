# Profiling

```bash
aibi profile model.json
```

Every `CALCULATE`, `FILTER`, `VAR` and `RETURN` adds weight. Weights of 5+
are flagged as heavy candidates for analysis.
