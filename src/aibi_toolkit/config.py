"""Per-project config for aibi-toolkit (TOML)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10: stdlib tomllib landed in 3.11
    tomllib = None  # type: ignore[assignment]

DEFAULTS: dict[str, str | int] = {
    "max_name_length": 64,
    "default_currency": "USD",
    "percent_decimals": 1,
}


def _parse_simple_toml(text: str) -> dict[str, Any]:
    """Minimal [section] key = value parser for when tomllib is unavailable."""
    data: dict[str, dict[str, Any]] = {}
    section: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            data.setdefault(section, {})
        elif "=" in line and section is not None:
            key, value = (part.strip() for part in line.split("=", 1))
            parsed: Any
            if value.startswith(("'", '"')):
                parsed = value[1:-1]
            elif value.lower() in ("true", "false"):
                parsed = value.lower() == "true"
            else:
                try:
                    parsed = int(value)
                except ValueError:
                    parsed = value
            data[section][key] = parsed
    return data


def load_config(path: str | Path) -> dict[str, str | int]:
    """Load aibi config from TOML, falling back to defaults."""
    p = Path(path)
    if not p.exists():
        return dict(DEFAULTS)
    text = p.read_text(encoding="utf-8")
    data = tomllib.loads(text) if tomllib is not None else _parse_simple_toml(text)
    return {**DEFAULTS, **data.get("aibi", {})}


def validate_config(cfg: dict[str, Any]) -> list[str]:
    """Return human-readable config errors (empty = valid)."""
    errors: list[str] = []
    if not isinstance(cfg.get("max_name_length"), int) or cfg["max_name_length"] < 1:
        errors.append("max_name_length must be a positive integer")
    if cfg.get("default_currency") not in ("USD", "EUR", "GBP", "INR"):
        errors.append("default_currency must be one of USD/EUR/GBP/INR")
    if not isinstance(cfg.get("percent_decimals"), int) or not 0 <= cfg["percent_decimals"] <= 4:
        errors.append("percent_decimals must be an integer 0-4")
    return errors


def default_config_toml() -> str:
    """Render a starter aibi.toml for users."""
    lines = ["[aibi]"]
    lines += [f"{k} = {v!r}" for k, v in DEFAULTS.items()]
    return "\n".join(lines) + "\n"
