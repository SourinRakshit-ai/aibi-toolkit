from aibi_toolkit.lint import lint_dax


def test_divide_warning():
    assert any("DIVIDE" in f for f in lint_dax("ASP = [Sales] / [Units]"))


def test_iferror():
    assert any("IFERROR" in f for f in lint_dax("X = IFERROR([A]/[B], 0)"))


def test_clean():
    assert lint_dax("ASP = DIVIDE([Sales], [Units], 0)") == []


def test_countrows_values_lint():
    flag = lint_dax
    assert any("DISTINCTCOUNT" in f for f in flag("COUNTROWS(VALUES('Sales'[Region])) + 1"))
    assert any("DISTINCTCOUNT" in f for f in flag("COUNTROWS( VALUES([Region]) )"))
    assert flag("COUNTROWS(Sales)") == []
    assert flag("RANGE(VALUES([Region]))") == []


def test_if_true_false_branch_lint():
    flag = lint_dax
    assert any("always x" in f for f in flag("IF(TRUE(), 1, 2)"))
    assert any("always y" in f for f in flag("IF(FALSE(), 1, 2)"))
    assert flag("IF([cond], 1, 2)") == []
    assert flag("IF([active], [a], [b])") == []


def test_if_true_case_insensitive():
    flag = lint_dax
    assert any("always x" in f for f in flag("IF(true(), 1, 2)"))
    assert any("always y" in f for f in flag("IF(FALSE(), 1, 2)"))


def test_not_not_rule():
    flag = lint_dax
    assert any("double wrapper" in f for f in flag("NOT(NOT([Active]))"))
    assert flag("NOT([Active])") == []
    assert flag("[x] != [y]") == []


def test_nested_trim_rule():
    flag = lint_dax
    assert any("TRIM(TRIM(x))" in f for f in flag("TRIM(TRIM([Name]))"))
    assert flag("TRIM([Name])") == []
    assert flag("TRIM(LOWER(TRIM([Name])))") == []


def test_nested_upper_rule():
    flag = lint_dax
    assert any("UPPER is idempotent" in f for f in flag("UPPER(UPPER([Name]))"))


def test_nested_lower_rule():
    flag = lint_dax
    assert any("LOWER is idempotent" in f for f in flag("LOWER(LOWER([Name]))"))


def test_nested_abs_rule():
    flag = lint_dax
    assert any("ABS is idempotent" in f for f in flag("ABS(ABS([x]))"))


def test_nested_int_rule():
    flag = lint_dax
    assert any("INT is idempotent" in f for f in flag("INT(INT([x]))"))
    assert flag("UPPER(LOWER([x]))") == []
    assert flag("ABS([x])") == []


def test_distinctcount_values_rule():
    flag = lint_dax
    assert any("DISTINCTCOUNT(x)" in f for f in flag("DISTINCTCOUNT(VALUES([Region]))"))
    assert flag("DISTINCTCOUNT([Region])") == []
    assert flag("COUNTROWS(VALUES([Region]))") != []


def test_true_comparison_rule():
    flag = lint_dax
    assert any("column is already" in f for f in flag("[Active] = TRUE()"))
    assert any("column is already" in f for f in flag("IF([Active] = TRUE(), 1, 2)"))
    assert all("column is already" not in f for f in flag("IF(TRUE(), 1, 2)"))


def test_false_comparison_rule():
    flag = lint_dax
    assert any("invert the column" in f for f in flag("[Active] = FALSE()"))
    assert flag("IF([Active], 1, 2)") == []


def test_abs_impossible_rule():
    flag = lint_dax
    assert any("can never hold" in f for f in flag("IF(ABS([x]) < 0, 1, 2)"))
    assert flag("IF(ABS([x]) >= 0, 1, 2)") == []
    assert flag("IF(ABS([x]) < [y], 1, 2)") == []
