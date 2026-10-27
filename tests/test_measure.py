from aibi_toolkit.measure import currency_format, percent_format, detect_format


def test_currency_usd():
    assert currency_format("USD") == "$#,0.00"


def test_currency_inr():
    assert currency_format("INR", 0) == "₹#,0"


def test_percent():
    assert percent_format(1) == "0.0%"


def test_detect_float():
    assert detect_format(12.5) == "#,0.00"
