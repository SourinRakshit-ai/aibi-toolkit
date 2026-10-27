"""DAX filter-context snippets."""


def build_topn_measure(measure: str, table: str, column: str, top: int = 10, name: str = "Top N") -> str:
    """Show a measure filtered to the top N items of a column."""
    return (
        f"{name} {measure} =\n"
        f"VAR _top = TOPN({top}, ALLSELECTED('{table}'), [{measure}])\n"
        f"RETURN CALCULATE([{measure}], KEEPFILTERS(_top))"
    )
