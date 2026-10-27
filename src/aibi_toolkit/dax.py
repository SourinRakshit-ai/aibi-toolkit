"""DAX snippet builders."""


def build_sum_measure(table: str, column: str, name: str) -> str:
    """SUM measure using the safe, readable pattern."""
    return (
        f"{name} =\n"
        f"VAR _rows = '{table}'\n"
        f"RETURN SUM(_rows[{column}])"
    )
