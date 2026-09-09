from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, closing

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import settings
from app.db import connect, migrate
from app.errors import NotFoundError, UnauthorizedError
from app.routes import events


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    with closing(connect(settings.DATABASE_PATH)) as conn:
        migrate(conn)
    yield


app = FastAPI(title="NEI Events", lifespan=lifespan)
app.include_router(events.router)


@app.exception_handler(UnauthorizedError)
def handle_unauthorized(_: Request, exc: UnauthorizedError) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(NotFoundError)
def handle_not_found(_: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})
