from aibi_toolkit.filters import build_topn_measure, build_isfiltered_check


def test_topn():
    dax = build_topn_measure("Total", "Sales", "Product", 5)
    assert "TOPN(5" in dax
    assert "KEEPFILTERS" in dax


def test_isfiltered():
    assert "ISFILTERED" in build_isfiltered_check()
