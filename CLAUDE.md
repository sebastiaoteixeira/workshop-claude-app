# NEI Events API

FastAPI + SQLite (stdlib `sqlite3`, no ORM) + Pydantic v2, managed with `uv`.

## Commands

- `make test`: the only way to run the suite (`pytest` alone does not see the environment)
- `make lint`: ruff check and format check; run it before finishing any task
- `make run`: dev server; `make seed` rebuilds `data/workshop.db`

## Layers

- `app/routes/`: HTTP handlers only. A new router is registered in `app/main.py`.
- `app/repositories/`: all SQL. Handlers never call `conn.execute`.
- `app/schemas.py`: every response is one of these models, never a dict.
- `app/errors.py`: raise these classes (`NotFoundError`, `ConflictError`, ...); the single
  handler in `app/main.py` maps them to status codes. Never raise `HTTPException`.

## Do not touch

- `migrations/*.sql` already applied: add a new numbered file instead of editing one.
- `.env`: local secrets. `.env.example` documents the variables.
