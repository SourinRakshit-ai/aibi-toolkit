# Naming conventions

- Tables: plain plural nouns ("Orders", "Customers")
- Columns: snake_case in source, Title Case for display
- Measures: aggregation prefix ("Total", "Count of", "Average")

## Anti-patterns

- Mixing abbreviations with full words in the same table
- Measure names that duplicate column names
- Spaces at the start or end of any object name

## Style conversions

`to_snake_case`, `kebab_case`, `pascal_case`, `to_display_name` — pick one
convention per layer and stick to it.
