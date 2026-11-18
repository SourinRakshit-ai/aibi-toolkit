# Passing a model to aibi

`aibi summary <path>` — every command on this page accepts the model as a
single path argument. `<path>` may be one of two shapes:

## 1. A shared-schema JSON dump

Produced by your model tool (Power BI Desktop, Tabular Editor, or the JSON
export in the Semantic Model Explorer). Top-level shape: an object with
`tables` and optional `relationships`, where each entry has `measures`,
`columns`, `name`, etc. JSON that fails a top-level shape check exits `2`
with a single-line stderr reason.

```bash
aibi summary model.json
aibi audit model.json
aibi lint model.json
```

## 2. A TMDL folder

If `<path>` is a directory, it must follow the PBIP folder layout:

```
<proj>/
├── <name>.Dataset/
│   └── definition/
│       ├── tables/
│       │   ├── Sales.tmdl
│       │   ├── Customer.tmdl
│       │   └── ...
│       ├── relationships.tmdl
│       └── model.tmdl
└── ...other project files
```

`load_model` walks `definition/tables/*.tmdl` and
`definition/relationships.tmdl`, parses the objects inside them, and feeds
the same model dict back into every command: `summary`, `tables`, `audit`,
`lint`, `profile`, `fix`, `export`, `report`, `diagram`.

```bash
aibi summary ./MyModel.Dataset
aibi audit ./MyModel.Dataset/definition
aibi lint ./MyModel.Dataset/definition
```

`.pbip` root, `*.Dataset` folder, or `definition/` itself are all accepted —
they end at the same TMDL entry point.

## What the loader parses

`tables/*.tmdl`:

- `table <Name>` declarations and the full table body
- `column <Name>` — `name`, `dataType`, `sourceColumn`, `sourceColumn`,
  `isHidden`
- `measure 'Name' = <expression>` — `expression` (single-line and
  multi-line DAX delimited by triple backticks), `formatString`

`relationships.tmdl`:

- `relationship <Name>` — `fromColumn`, `toColumn`, `isActive`,
  `crossFilterDirection`, `cardinality`

Everything else (hierarchies, partitions, cultures, roles, perspectives,
functions, expressions, annotations) is silently skipped — the toolkit
only cares about what feeds the shared model dict.

## Input format choice

Use the JSON dump when your model tool offers one and you want one
authored file that stays versioned. Use a TMDL folder when you need
changes committed in your model repository or when you want to inspect
an in-flight project before exporting anything.

Both paths go through the identical downstream code — there is no other
difference between JSON and TMDL input.
