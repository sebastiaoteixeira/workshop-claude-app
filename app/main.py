from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, closing

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import settings
from app.db import connect, migrate
from app.errors import ApiError
from app.routes import events, health, registrations, waitlist


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    with closing(connect(settings.DATABASE_PATH)) as conn:
        migrate(conn)
    yield


app = FastAPI(title="NEI Events", lifespan=lifespan)
app.include_router(health.router)
app.include_router(events.router)
app.include_router(registrations.router)
app.include_router(waitlist.router)


@app.exception_handler(ApiError)
def handle_api_error(_: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})
