from aibi_toolkit.dax import build_sum_measure, build_safe_ratio


def test_sum_measure():
    dax = build_sum_measure("Sales", "Amount", "Total Sales")
    assert dax.startswith("Total Sales =")
    assert "SUM" in dax


def test_safe_ratio():
    dax = build_safe_ratio("Sales", "Units", "ASP")
    assert "DIVIDE" in dax


def test_cumulative():
    from aibi_toolkit.dax import build_cumulative_measure
    dax = build_cumulative_measure("Total", "'Calendar'[Date]", "Cum Total")
    assert "MAX" in dax and "CALCULATE" in dax
