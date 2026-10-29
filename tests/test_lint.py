from aibi_toolkit.lint import lint_dax


def test_divide_warning():
    assert any("DIVIDE" in f for f in lint_dax("ASP = [Sales] / [Units]"))


def test_iferror():
    assert any("IFERROR" in f for f in lint_dax("X = IFERROR([A]/[B], 0)"))


def test_clean():
    assert lint_dax("ASP = DIVIDE([Sales], [Units], 0)") == []
