# Linting DAX

```bash
aibi lint model.json
```

Rules:
- Prefer `DIVIDE` over `/`
- Avoid `IFERROR` (hides real errors)
- Avoid no-argument `ALLSELECTED`
