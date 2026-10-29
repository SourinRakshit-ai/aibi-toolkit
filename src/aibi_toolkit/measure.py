"""Format-string helpers for DAX measures."""

CURRENCY_SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}


def currency_format(code: str, decimals: int = 2) -> str:
    """Build a currency format string, e.g. $#,0.00."""
    symbol = CURRENCY_SYMBOLS.get(code.upper(), code)
    return f"{symbol}#,0.{('0' * decimals) if decimals else ''}".rstrip(".")


def percent_format(decimals: int = 1) -> str:
    """Build a percentage format string, e.g. 0.0%."""
    return f"0.{('0' * decimals) if decimals else ''}%"


def thousands_format(decimals: int = 0) -> str:
    """Build a thousands-separated format string, e.g. #,0.00."""
    return f"#,0.{('0' * decimals) if decimals else ''}".rstrip(".")


def detect_format(sample_value) -> str:
    """Guess a format string from a sample numeric value."""
    if isinstance(sample_value, bool):
        return "TRUE/FALSE"
    if isinstance(sample_value, int):
        return "#,0"
    if isinstance(sample_value, float):
        if abs(sample_value) < 10:
            return percent_format(1)
        return "#,0.00"
    raise TypeError(f"Unsupported sample type: {type(sample_value)!r}")


DATE_FORMATS = {"short": "dd/MM/yyyy", "iso": "yyyy-MM-dd", "long": "d MMMM yyyy"}


def date_format(style: str = "short") -> str:
    """Look up a date format string by style name."""
    return DATE_FORMATS[style]


def format_report(model: dict, path) -> None:
    """Apply detected formats to every numeric measure and write a report."""
    import csv as _csv
    from pathlib import Path as _Path
    with _Path(path).open("w", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        w.writerow(["table", "name", "suggested_format"])
        for t in model.get("tables", []):
            for m in t.get("measures", []):
                if m.get("expression", "").startswith("SUM"):
                    w.writerow([t["name"], m["name"], "#,0.00"])


def merge_formats(*maps: dict) -> dict:
    """Merge format maps, later maps winning on conflicts."""
    out: dict = {}
    for m in maps:
        out.update(m)
    return out


def smart_format(value: float, currency: str = "USD") -> str:
    """Pick currency vs plain format based on value magnitude."""
    if value >= 1000:
        return currency_format(currency)
    if value < 1:
        return percent_format(2)
    return thousands_format(2)


FORMAT_ALIASES = {
    "money": "$#,0.00",
    "pct": "0.0%",
    "count": "#,0",
    "seconds": "#,0.0 s",
}


def resolve_format(key: str) -> str:
    """Resolve a friendly alias to a full format string."""
    try:
        return FORMAT_ALIASES[key]
    except KeyError:
        raise ValueError(f"Unknown format alias: {key!r}") from None


SHORT_SCALE = [("", 1), ("K", 1_000), ("M", 1_000_000), ("B", 1_000_000_000)]


def human_readable(value: float) -> str:
    """Render a number like 1.2M / 340K for CLI and docs output."""
    for suffix, scale in reversed(SHORT_SCALE):
        if abs(value) >= scale and scale > 1:
            return f"{value / scale:.1f}{suffix}"
        if scale == 1:
            return f"{value:,.0f}"
    return str(value)


def format_key_from_format(fmt: str) -> str:
    """Map a format string to a stable category key for grouping."""
    if fmt.endswith("%"):
        return "percent"
    if fmt.count(",") and "$" in fmt:
        return "currency"
    return "number"
