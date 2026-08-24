.PHONY: bootstrap fixtures schemas format lint typecheck test build package-check check

bootstrap:
	python -m pip install -r requirements-dev.txt
	python -m pip install -e .

fixtures:
	PYTHONPATH=src python scripts/build_fixtures.py

schemas:
	PYTHONPATH=src python scripts/export_schemas.py

format:
	ruff format .

lint:
	ruff check .
	ruff format --check .

typecheck:
	mypy src

test:
	pytest

build:
	python -m pip wheel --no-deps --wheel-dir dist .

package-check: build
	python scripts/check_package.py

check: fixtures schemas lint typecheck test package-check
