"""Format-string helpers for DAX measures."""

CURRENCY_SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}


def currency_format(code: str, decimals: int = 2) -> str:
    """Build a currency format string, e.g. $#,0.00."""
    symbol = CURRENCY_SYMBOLS.get(code.upper(), code)
    return f"{symbol}#,0.{('0' * decimals) if decimals else ''}"


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
