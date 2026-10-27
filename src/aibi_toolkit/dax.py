"""DAX snippet builders."""


def build_sum_measure(table: str, column: str, name: str) -> str:
    """SUM measure using the safe, readable pattern."""
    return (
        f"{name} =\n"
        f"VAR _rows = '{table}'\n"
        f"RETURN SUM(_rows[{column}])"
    )


def build_distinctcount_measure(table: str, column: str, name: str) -> str:
    """DISTINCTCOUNT measure snippet."""
    return f"{name} =\nDISTINCTCOUNT('{table}'[{column}])"


def build_safe_ratio(numerator: str, denominator: str, name: str, alt: str = "0") -> str:
    """Ratio wrapped in DIVIDE so divide-by-zero never errors."""
    return f"{name} =\nDIVIDE([{numerator}], [{denominator}], {alt})"
