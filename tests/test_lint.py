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


def test_countrows_zero_rule():
    flag = lint_dax
    assert any("ISEMPTY" in f for f in flag("IF(COUNTROWS([T]) = 0, 1, 2)"))
    assert any("ISEMPTY" in f for f in flag("IF(0 = COUNTROWS([T]), 1, 2)"))
    assert flag("COUNTROWS([T]) > 0") == []


def test_blank_equality_rule():
    flag = lint_dax
    assert any("ISBLANK" in f for f in flag("[x] = BLANK()"))
    assert flag("ISBLANK([x])") == []


def test_blank_inequality_rule():
    flag = lint_dax
    assert any("NOT(ISBLANK" in f for f in flag("[x] <> BLANK()"))
    assert flag("[x] > BLANK()") == []


def test_rule_catalog_names_are_unique_and_stable():
    from aibi_toolkit.lint import RULES

    names = [rule.name for rule in RULES]
    assert len(names) == len(set(names)), "duplicate rule names break explain"
    assert names[0] == "raw_division"
    assert "double_negation" in names
    assert "blank_inequality" in names
    assert all(rule.message for rule in RULES)


def test_lint_findings_keep_rule_attribution():
    from aibi_toolkit.lint import lint_findings

    found = lint_findings("NOT(NOT([x])) + [y] / [z]")
    names = [name for name, _ in found]
    assert names == ["raw_division", "double_negation"]
    assert [msg for _, msg in found] == lint_dax("NOT(NOT([x])) + [y] / [z]")


def test_cli_list_rules_and_explain(capsys):
    from aibi_toolkit.cli import main

    assert main(["lint", "--list-rules"]) == 0
    listed = capsys.readouterr().out
    assert "double_negation" in listed
    assert "raw_division" in listed

    assert main(["explain", "double_negation"]) == 0
    explained = capsys.readouterr().out
    assert "double_negation" in explained
    assert "pattern:" in explained

    assert main(["explain", "nope"]) == 2
    assert "unknown rule" in capsys.readouterr().err


def test_sarif_document_shape_and_attribution():

    from aibi_toolkit.lint import lint_model_findings
    from aibi_toolkit.sarif import build_sarif

    model = {
        "tables": [
            {
                "name": "Sales",
                "columns": [],
                "measures": [
                    {"name": "Dirty/Measure", "expression": "NOT(NOT([x])) + [a] / [b]"}
                ],
            }
        ]
    }
    doc = build_sarif(lint_model_findings(model), "model.json")
    assert doc["version"] == "2.1.0"
    assert doc["$schema"].endswith("sarif-2.1.0.json")
    run = doc["runs"][0]
    assert run["tool"]["driver"]["name"] == "aibi-toolkit"
    assert len(run["tool"]["driver"]["rules"]) == 20
    ids = [r["ruleId"] for r in run["results"]]
    assert ids == ["raw_division", "double_negation"]
    uri = run["results"][0]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
    assert uri == "model.json#/tables/Sales/measures/Dirty~1Measure"


def test_cli_sarif_conflicts_with_json(capsys, tmp_path):
    import json as _json

    from aibi_toolkit.cli import main

    model = tmp_path / "dirty.json"
    model.write_text(
        _json.dumps(
            {"tables": [{"name": "Sales", "columns": [], "measures": [
                {"name": "M", "expression": "NOT(NOT([x])) + [a] / [b]"}
            ]}]}
        ),
        encoding="utf-8",
    )
    model = str(model)
    assert main(["lint", model, "--sarif"]) == 0
    doc = _json.loads(capsys.readouterr().out)
    assert doc["version"] == "2.1.0"
    assert main(["lint", model, "--sarif", "--json"]) == 2
    assert "mutually exclusive" in capsys.readouterr().err


def test_raw_division_constant_denominator_is_safe():
    assert lint_dax("[x] / 2") == []
    assert lint_dax("1 / 2") == []
    assert any("DIVIDE" in f for f in lint_dax("[x] / [y]"))
    assert lint_dax("ASP = DIVIDE([Sales], [Units], 0)") == []


def test_strict_equality_is_not_plain_equality():
    for expr in ("[x] == TRUE()", "[x] == FALSE()", "[x] == BLANK()"):
        assert lint_dax(expr) == [], expr
    assert any("column is already" in f for f in lint_dax("[x] = TRUE()"))
    assert any("ISBLANK" in f for f in lint_dax("[x] = BLANK()"))


def test_cli_lint_rule_filter_all_formats(capsys, tmp_path):
    import json as _json

    from aibi_toolkit.cli import main

    model = tmp_path / "dirty.json"
    model.write_text(
        _json.dumps({"tables": [{"name": "Sales", "columns": [], "measures": [
            {"name": "M", "expression": "[a] / [b] + NOT(NOT([x]))"}
        ]}]}),
        encoding="utf-8",
    )
    assert main(["lint", str(model), "--rule", "raw_division"]) == 1
    out = capsys.readouterr().out
    assert "DIVIDE" in out and "double wrapper" not in out

    assert main(["lint", str(model), "--rule", "raw_division", "--json"]) == 1
    payload = _json.loads(capsys.readouterr().out)["lint"]
    assert payload == {"M": ["use DIVIDE instead of / to guard divide-by-zero"]}

    assert main(["lint", str(model), "--rule", "raw_division", "--sarif"]) == 0
    doc = _json.loads(capsys.readouterr().out)
    assert [r["ruleId"] for r in doc["runs"][0]["results"]] == ["raw_division"]
    assert len(doc["runs"][0]["tool"]["driver"]["rules"]) == 1


def test_cli_lint_unknown_rule_exits_two(capsys, tmp_path):
    from aibi_toolkit.cli import main

    model = tmp_path / "clean.json"
    model.write_text("{}", encoding="utf-8")
    assert main(["lint", str(model), "--rule", "nope"]) == 2
    assert "unknown rule" in capsys.readouterr().err
