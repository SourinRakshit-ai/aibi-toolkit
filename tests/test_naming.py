from aibi_toolkit.naming import to_snake_case, to_display_name


def test_snake_case():
    assert to_snake_case("Total Sales Amount") == "total_sales_amount"


def test_snake_case_camel():
    assert to_snake_case("salesAmountYTD") == "sales_amount_ytd"


def test_display_name():
    assert to_display_name("total_sales_amount") == "Total Sales Amount"
