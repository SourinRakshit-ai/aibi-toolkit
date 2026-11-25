from aibi_toolkit.naming import to_display_name, to_snake_case


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


def test_kebab():
    from aibi_toolkit.naming import kebab_case
    assert kebab_case("Total Sales") == "total-sales"


def test_strip_numbers():
    from aibi_toolkit.naming import strip_numbers
    assert strip_numbers("Orders 2") == "Orders"


def test_pluralize():
    from aibi_toolkit.naming import pluralize
    assert pluralize("Order") == "Orders"
    assert pluralize("Category") == "Categories"
    assert pluralize("Box") == "Boxes"


def test_split_words():
    from aibi_toolkit.naming import split_words
    assert split_words("totalSales hintText") == ["total", "Sales", "hint", "Text"]


def test_initials():
    from aibi_toolkit.naming import initials
    assert initials("Total Sales") == "TS"


def test_a_or_an_pronunciation_exceptions():
    from aibi_toolkit.naming import a_or_an

    assert a_or_an("hour") == "an"
    assert a_or_an("honest") == "an"
    assert a_or_an("user") == "a"
    assert a_or_an("unique") == "a"
    assert a_or_an("apple") == "an"
    assert a_or_an("table") == "a"
    assert a_or_an("") == "a"


def test_a_or_an_case_plural_and_phrase():
    from aibi_toolkit.naming import a_or_an

    assert a_or_an("Hours") == "an"
    assert a_or_an("honest answer") == "an"
    assert a_or_an("Unicode") == "a"
    assert a_or_an("one measure") == "a"
    assert a_or_an("apple") == "an"
    assert a_or_an("table") == "a"


def test_split_words_acronym_boundaries():
    from aibi_toolkit.naming import split_words

    assert split_words("XMLHttp") == ["XML", "Http"]
    # acronym boundary is before the capital that starts the lowercase word
    assert split_words("ABCdef") == ["AB", "Cdef"]
    assert split_words("HTTPResponseCode") == ["HTTP", "Response", "Code"]
    assert split_words("TotalSales") == ["Total", "Sales"]
    assert split_words("snake_case") == ["snake", "case"]
