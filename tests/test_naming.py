from aibi_toolkit.naming import to_snake_case, to_display_name


def test_snake_case():
    assert to_snake_case("Total Sales Amount") == "total_sales_amount"


def test_snake_case_camel():
    assert to_snake_case("salesAmountYTD") == "sales_amount_ytd"


def test_display_name():
    assert to_display_name("total_sales_amount") == "Total Sales Amount"


def test_truncate():
    from aibi_toolkit.naming import truncate_name
    assert truncate_name("abcdefgh", 4) == "abcd"


def test_dedupe():
    from aibi_toolkit.naming import dedupe_names
    assert dedupe_names(["Rev", "Rev"]) == ["Rev", "Rev 2"]


def test_normalize_all():
    from aibi_toolkit.naming import normalize_all
    assert normalize_all(["Cust Amt", "cust amt"]) == ["customer amount", "customer amount 2"]


def test_pascal():
    from aibi_toolkit.naming import pascal_case
    assert pascal_case("total_sales_amount") == "TotalSalesAmount"


def test_validate():
    from aibi_toolkit.naming import validate_name
    assert validate_name(" good name ") == ["leading/trailing whitespace"]
