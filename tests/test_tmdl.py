"""Tests for the TMDL loader: a .pbip folder feeds into the same model dict."""

from __future__ import annotations

import json
from pathlib import Path

from aibi_toolkit.metadata import list_measures, list_tables, load_model, model_summary
from aibi_toolkit.tmdl import load_pbip

FIXTURE = Path(__file__).parent / "fixtures" / "pbip"


def test_load_pbip_reads_tables_measures_columns():
    model = load_pbip(FIXTURE)
    by_name = {t["name"]: t for t in model["tables"]}
    assert set(by_name) == {"Sales", "Customer", "Date"}

    sales = by_name["Sales"]
    measures = {m["name"]: m for m in sales["measures"]}
    assert measures["Total Sales"]["formatString"] == "$ #,##0.00"
    assert "SUMX" in measures["Total Sales"]["expression"]
    assert measures["No Format Measure"].get("formatString") is None
    assert len(sales["columns"]) == 4

    customer = by_name["Customer"]
    assert [m["name"] for m in customer["measures"]] == ["# Customers"]

    date = by_name["Date"]
    assert date["measures"] == []
    assert len(date["columns"]) == 1


def test_load_pbip_reads_relationships_into_shared_schema():
    model = load_pbip(FIXTURE)
    by_tab = {(r["fromTable"], r["toTable"]): r for r in model["relationships"]}
    assert by_tab[("Sales", "Date")]["fromColumn"] == "OrderDate"
    assert by_tab[("Sales", "Date")]["isActive"] is True
    assert by_tab[("Sales", "Customer")]["isActive"] is False


def test_summary_and_list_work_on_tmdl():
    model = load_model(str(FIXTURE))
    counts = model_summary(model)
    assert counts["tables"] == 3
    assert counts["measures"] == 4
    assert counts["columns"] == 7
    assert set(list_tables(model)) == {"Sales", "Customer", "Date"}
    names = {(m["table"], m["name"]) for m in list_measures(model)}
    assert ("Sales", "Total Sales") in names
    assert ("Customer", "# Customers") in names


def test_load_model_dispatches_directory_to_tmdl(tmp_path):
    # a directory is walked for a TMDL definition/, not read as JSON
    json_dir = tmp_path / "fixture.json"
    json_dir.write_text(json.dumps({"tables": [{"name": "JSONTable", "columns": [], "measures": []}]}))
    loaded_json = load_model(str(json_dir))
    assert loaded_json["tables"][0]["name"] == "JSONTable"

    loaded_tmdl = load_model(str(FIXTURE))
    assert {t["name"] for t in loaded_tmdl["tables"]} == {"Sales", "Customer", "Date"}


def test_load_model_directory_without_definition_is_a_clear_error(tmp_path):
    try:
        load_pbip(tmp_path)
    except ValueError as exc:
        assert "no TMDL tables" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_definition_folder_directly_is_accepted():
    direct = FIXTURE / "definition"
    model = load_pbip(direct)
    assert {t["name"] for t in model["tables"]} == {"Sales", "Customer", "Date"}


def test_summed_measure_expression_survives_roundtrip():
    measures = {m["name"]: m for m in load_pbip(FIXTURE)["tables"][2]["measures"]}
    assert measures["Total Sales"]["expression"] == "SUMX(\n\tSales,\n\tSales[Quantity]\n)"


def test_cli_path_loads_tmdl_folder():
    from aibi_toolkit.cli import main

    rc = main(["summary", str(FIXTURE)])
    assert rc == 0


def test_cli_audit_subcommand_on_tmdl_fixture():
    from aibi_toolkit.cli import main

    rc = main(["audit", str(FIXTURE)])
    assert rc in (0, 1)
