# Linting DAX

```bash
aibi lint model.json
```

Rules:
- Prefer `DIVIDE` over `/`
- Avoid `IFERROR` (hides real errors)
- Avoid no-argument `ALLSELECTED`

## Rule list

| Rule                  | Why                        |
| --------------------- | -------------------------- |
| divert-by-DIVIDE      | divide-by-zero errors      |
| no IFERROR            | hides real failures        |
| no bare ALLSELECTED() | ambiguous in visuals       |
