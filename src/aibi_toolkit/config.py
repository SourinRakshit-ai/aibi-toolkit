"""Per-project config for aibi-toolkit (TOML)."""

from pathlib import Path
import tomllib

DEFAULTS = {
    "max_name_length": 64,
    "default_currency": "USD",
    "percent_decimals": 1,
}


def load_config(path) -> dict:
    """Load aibi config from TOML, falling back to defaults."""
    p = Path(path)
    if not p.exists():
        return dict(DEFAULTS)
    data = tomllib.loads(p.read_text(encoding="utf-8"))
    return {**DEFAULTS, **data.get("aibi", {})}


def validate_config(cfg: dict) -> list[str]:
    """Return human-readable config errors (empty = valid)."""
    errors = []
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
    lines += [f'{k} = {v!r}' for k, v in DEFAULTS.items()]
    return "\n".join(lines) + "\n"
