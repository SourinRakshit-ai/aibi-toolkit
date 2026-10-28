# Auditing

```bash
aibi audit model.json
```

Exits non-zero when findings exist, so it works as a CI gate:

```yaml
- run: aibi audit model.json
```
