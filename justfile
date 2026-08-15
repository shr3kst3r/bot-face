default: verify

verify: lint format-check typecheck test

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

format:
	uv run ruff format .

typecheck:
	uv run ty check src

test:
	uv run pytest -q

help:
	uv run bf --help

hooks:
	uv run pre-commit install

hooks-run:
	uv run pre-commit run --all-files
