.PHONY: test lint run seed

ENV_FILE := $(wildcard .env)
UV_RUN := uv run $(ENV_FILE:%=--env-file %)

test:
	uv run pytest -q

lint:
	uv run ruff check .
	uv run ruff format --check .

run:
	$(UV_RUN) uvicorn app.main:app --reload

seed:
	$(UV_RUN) python -m scripts.seed
