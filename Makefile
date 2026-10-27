.PHONY: test lint clean

test:
	pytest -q

lint:
	python -m compileall -q src tests

clean:
	rm -rf dist .pytest_cache __pycache__
