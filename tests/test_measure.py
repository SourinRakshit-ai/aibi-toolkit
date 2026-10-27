from aibi_toolkit.measure import currency_format, percent_format, detect_format


def test_currency_usd():
    assert currency_format("USD") == "$#,0.00"


def test_currency_inr():
    assert currency_format("INR", 0) == "₹#,0"


def test_percent():
    assert percent_format(1) == "0.0%"


def test_detect_float():
    assert detect_format(12.5) == "#,0.00"


def test_smart_format_currency():
    from aibi_toolkit.measure import smart_format
    assert smart_format(5000) == "$#,0.00"


def test_resolve_format():
    from aibi_toolkit.measure import resolve_format
    assert resolve_format("pct") == "0.0%"
