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
