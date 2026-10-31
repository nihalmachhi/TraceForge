.PHONY: install lint types test demo serve gate site-build site-dev

install:
	python -m pip install -e ".[dev]"

lint:
	python -m ruff check src tests scripts
	python -m ruff format --check src tests scripts

format:
	python -m ruff format src tests scripts

types:
	python -m mypy --strict src

test:
	python -m pytest --cov=traceforge.core --cov=traceforge.privacy --cov=traceforge.storage --cov=traceforge.evaluation

demo:
	python -m traceforge demo

serve:
	python -m traceforge serve

gate:
	python -m traceforge gate

site-build:
	cd site && npm ci && npm run build

site-dev:
	cd site && npm run dev
