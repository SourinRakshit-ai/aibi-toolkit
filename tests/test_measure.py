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


def test_human_readable():
    from aibi_toolkit.measure import human_readable
    assert human_readable(1_240_000) == "1.2M"
    assert human_readable(340) == "340"


def test_format_key():
    from aibi_toolkit.measure import format_key_from_format
    assert format_key_from_format("0.0%") == "percent"
    assert format_key_from_format("$#,0.00") == "currency"
    assert format_key_from_format("#,0") == "number"


def test_validate_format():
    from aibi_toolkit.measure import validate_format
    assert validate_format("0.0%$") == ["mixes percent and currency tokens"]
    assert validate_format("#,0") == []


def test_scale():
    from aibi_toolkit.measure import scale_number
    assert scale_number(1.005) == 1.0
