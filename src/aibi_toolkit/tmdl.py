"""Load a `.pbip`-style TMDL semantic-model folder into the shared model dict.

The whole toolkit reads one shape: `Model = {"tables": [...], "relationships": [...]}`.
JSON dumps and TMDL folders produce exactly that same dict, so every command
keeps working on either input. Use `metadata.load_model(path)` for either.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

Model = dict[str, Any]

_TMDL_NAME = re.compile(r"^\s*'((?:[^']|'')*)'|^\s*(\S+)")


def _strip_desc(line: str) -> str | None:
    """Return the description text if this is a `/// ...` line, else None."""
    s = line.strip()
    if s.startswith("///"):
        return s[3:].strip()
    return None


def _parse_measure_name(line: str) -> tuple[str, str] | None:
    """Parse `measure 'Name' = <start-of-expr>` or `measure Name = <start-of-expr>`."""
    m = re.match(r"^(?P<comment>\s*)(?P<kw>measure)\s+(?P<rest>.*)$", line, re.IGNORECASE)
    if not m:
        return None
    rest = m.group("rest")
    if "=" not in rest:
        return None
    head, sep, tail = rest.partition("=")
    if sep != "=":
        return None
    return _tmdl_name(head.strip()), tail.strip()


def _dedent(text: str) -> str:
    lines = text.splitlines()
    stripped = [line for line in lines if line.strip()]
    if not stripped:
        return ""
    margin = min(len(line) - len(line.lstrip(" \t")) for line in stripped)
    return "\n".join(line[margin:] for line in lines).strip("\n")


def _tmdl_name(raw: str) -> str:
    """Unquote a TMDL name and unescape doubled quotes."""
    raw = raw.strip()
    if raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
        inner = raw[1:-1]
        return inner.replace("''", "'")
    return raw


def _parse_table_tmdl(text: str) -> Model:
    tables: list[dict[str, Any]] = []
    table: dict[str, Any] | None = None
    measure: dict[str, Any] | None = None
    node: dict[str, Any] | None = None  # object current properties attach to
    in_measure_block = False
    block_lines: list[str] = []

    for raw in text.splitlines():
        stripped = raw.rstrip()
        s = stripped.strip()
        if not s or s.startswith("//"):
            continue
        _ = _strip_desc(s)  # descriptions are legal but carry no model data
        first, _, rest = s.partition(" ")

        if in_measure_block:
            assert node is not None
            close = re.match(r"^\s*```\s*$", s)
            if close:
                body = "\n".join(block_lines[1:]).strip("\n")
                node["expression"] = _dedent(body)
                in_measure_block = False
                continue
            block_lines.append(stripped)
            continue

        if first.lower() == "table":
            table = {"name": _tmdl_name(rest.strip()), "columns": [], "measures": []}
            tables.append(table)
            node = table
            measure = None
            continue

        if table is None:
            continue

        if first.lower() == "measure":
            named = _parse_measure_name(stripped)
            if named is None:
                continue
            name, expr_start = named
            measure = {"name": name, "expression": expr_start}
            table["measures"].append(measure)
            node = measure
            if expr_start.strip() == "```":
                in_measure_block = True
                block_lines = ["```"]
            continue

        if first.lower() == "column":
            col = {"name": _tmdl_name(rest.strip())}
            table["columns"].append(col)
            node = col
            measure = None
            continue

        if first.lower() in {"partition", "hierarchy", "calendar",
                             "calculationGroup", "expression", "annotation"}:
            # accepted but not needed for the toolkit's checks
            node = None
            measure = None
            continue

        if node is not None and ":" not in s and s.startswith("isHidden"):
            node["isHidden"] = True
            continue

        if node is not None and ":" in s:
            key, _, value = s.partition(":")
            key, value = key.strip().lower(), value.strip()
            if not key:
                continue
            fields = {
                "datatype": "dataType",
                "sourcecolumn": "sourceColumn",
                "formatstring": "formatString",
                "summarizeby": "summarizeBy",
                "sortbycolumn": "sortByColumn",
                "fromcolumn": "fromColumn",
                "tocolumn": "toColumn",
                "cardinality": "cardinality",
            }
            if key == "isactive":
                node["isActive"] = value.lower() != "false"
            elif key == "crossfilteringbehavior":
                node["crossFilterDirection"] = "both" if value.lower().startswith("both") else "one"
            elif key in fields:
                node[fields[key]] = value
            continue

    return {"tables": tables}


def _parse_relationship_tmdl(text: str) -> list[dict[str, Any]]:
    rels: list[dict[str, Any]] = []
    node: dict[str, Any] | None = None

    for raw in text.splitlines():
        s = raw.strip()
        if not s or s.startswith(("///", "//")):
            continue
        first, _, rest = s.partition(" ")

        if first.lower() == "relationship":
            node = {}
            rels.append(node)
            parsed = _tmdl_name(rest.strip())
            node["name"] = parsed
            node["isActive"] = True
            continue

        if node is not None and ":" in s:
            key, _, value = s.partition(":")
            key, value = key.strip(), value.strip()
            lowered = key.lower()
            if lowered == "fromcolumn":
                node["fromColumn"] = value
            elif lowered == "tocolumn":
                node["toColumn"] = value
            elif lowered == "isactive":
                node["isActive"] = value.lower() != "false"
            elif lowered == "crossfilteringbehavior":
                node["crossFilterDirection"] = "both" if value.lower().startswith("both") else "one"
            elif lowered == "cardinality":
                node["cardinality"] = value
            continue

    out: list[dict[str, Any]] = []
    for r in rels:
        from_col = r.get("fromColumn", "")
        to_col = r.get("toColumn", "")
        from_table, _, _ = from_col.partition(".")
        to_table, _, _ = to_col.partition(".")
        out.append(
            {
                "fromTable": _tmdl_name(from_table or "?"),
                "toTable": _tmdl_name(to_table or "?"),
                "fromColumn": _tmdl_name(from_col.partition(".")[2].strip() if "." in from_col else from_col),
                "toColumn": _tmdl_name(to_col.partition(".")[2].strip() if "." in to_col else to_col),
                "isActive": r.get("isActive", True),
                "crossFilterDirection": r.get("crossFilterDirection", "one"),
                "cardinality": r.get("cardinality"),
            }
        )
    return out


def _find_definition(path: Path) -> Path | None:
    """Locate the `definition/` folder for a .pbip project root, dataset or definition dir."""
    if (path / "tables").is_dir():
        return path
    direct = path / "definition"
    if (direct / "tables").is_dir():
        return direct
    for folder in path.iterdir() if path.is_dir() else []:
        if folder.is_dir():
            nested = folder / "definition"
            if (nested / "tables").is_dir():
                return nested
    if path.is_dir():
        deep = list(path.rglob("definition/tables"))
        if deep:
            return deep[0].parent
    return None


def load_pbip(path: str | Path) -> Model:
    """Load a TMDL folder into the shared model dict; raises ValueError if not found.

    Args accept a .pbip project root, a `*.Dataset` folder, or a direct
    `definition/` directory. Tables in `definition/tables/*.tmdl` and
    relationships in `definition/relationships.tmdl` are parsed; anything
    else is ignored.
    """
    root = Path(path)
    if not root.is_dir():
        raise ValueError(f"path is not a directory: {root}")

    definition = _find_definition(root)
    if definition is None:
        raise ValueError(
            f"no TMDL tables found under {root} — expected definition/tables/*.tmdl"
        )

    tables: list[dict[str, Any]] = []
    for tmdl in sorted((definition / "tables").glob("*.tmdl")):
        tables.extend(_parse_table_tmdl(tmdl.read_text(encoding="utf-8"))["tables"])

    relationships: list[dict[str, Any]] = []
    rels = definition / "relationships.tmdl"
    if rels.is_file():
        relationships.extend(_parse_relationship_tmdl(rels.read_text(encoding="utf-8")))

    return {"tables": tables, "relationships": relationships}
