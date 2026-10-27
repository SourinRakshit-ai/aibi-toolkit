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
