# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.2.x   | yes       |
| < 1.2   | no        |

## Reporting a Vulnerability

aibi-toolkit is a local CLI that reads JSON/TOML/CSV files you point it at.
It makes no network calls by default, but we still take vulnerabilities
seriously — especially path handling and parse bugs in `config.py` and
`csvio.py` that could execute unexpected content.

- Use GitHub's private vulnerability reporting (Security tab → Report a
  vulnerability) rather than a public issue.
- Expect an acknowledgement within 72 hours and a fix prompt for anything
  exploitable.

Please include a minimal reproduction (sample JSON/CSV is fine — the `aibi synth`
command generates one) so fixes go faster.
