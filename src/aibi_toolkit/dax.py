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


def build_ytd_measure(base: str, date_column: str, name: str) -> str:
    """Year-to-date measure over a base measure."""
    return (
        f"{name} =\n"
        f"TOTALYTD([{base}], '{date_column.split('.')[0] if '.' in date_column else date_column}')"
    )


def build_mom_measure(base: str, name: str) -> str:
    """Month-over-month measure over a base measure."""
    return (
        f"{name} =\n"
        f"VAR _prev = CALCULATE([{base}], PREVIOUSMONTH())\n"
        f"RETURN DIVIDE([{base}] - _prev, _prev)"
    )


def build_rank_measure(column: str, name: str) -> str:
    """Rank measure snippet."""
    return (
        f"{name} =\n"
        f"RANKX(ALLSELECTED(), [{column}], , DESC, DENSE)"
    )
