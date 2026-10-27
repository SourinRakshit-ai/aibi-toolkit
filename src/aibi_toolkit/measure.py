"""Format-string helpers for DAX measures."""

CURRENCY_SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}


def currency_format(code: str, decimals: int = 2) -> str:
    """Build a currency format string, e.g. $#,0.00."""
    symbol = CURRENCY_SYMBOLS.get(code.upper(), code)
    return f"{symbol}#,0.{('0' * decimals) if decimals else ''}"
