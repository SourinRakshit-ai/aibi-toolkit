.PHONY: install test typecheck lint build serve-docs

install:
	pip install -e ".[dev]"

test:
	pytest -q

typecheck:
	mypy --strict src/aibi_toolkit/

lint:
	ruff check src/ tests/

build:
	python -m build

serve-docs:
	mkdocs serve
