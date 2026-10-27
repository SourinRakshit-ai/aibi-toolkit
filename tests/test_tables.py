from aibi_toolkit.tables import markdown_table, align_column


def test_markdown_table():
    out = markdown_table([{"name": "Total", "fmt": "#,0"}])
    assert out.splitlines()[0].startswith("| name")
    assert "---" in out


def test_align():
    rows = align_column([{"n": "a"}, {"n": "bbb"}], "n")
    assert rows[1]["n"] == "bbb"
    assert rows[0]["n"] == "a  "
