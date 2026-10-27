"""DAX filter-context snippets."""


def build_topn_measure(measure: str, table: str, column: str, top: int = 10, name: str = "Top N") -> str:
    """Show a measure filtered to the top N items of a column."""
    return (
        f"{name} {measure} =\n"
        f"VAR _top = TOPN({top}, ALLSELECTED('{table}'), [{measure}])\n"
        f"RETURN CALCULATE([{measure}], KEEPFILTERS(_top))"
    )


def build_contains_filter(table: str, column: str, values: list[str], name: str = "Filtered") -> str:
    """Snippet filtering a table by a list of values."""
    joined = ", ".join(f'"{v}"' for v in values)
    return f"{name} =\nCALCULATE([Selected Measure], FILTER('{table}', '{table}'[{column}] IN {{{joined}}}))"


def build_isfiltered_check(name: str = "Has Filter") -> str:
    """Guard measure that reports whether a visual has cross-filtering."""
    return f"{name} =\nIF(ISFILTERED(), 1, 0)"
