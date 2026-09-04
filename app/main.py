from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, closing

from fastapi import FastAPI

from app import settings
from app.db import connect, migrate
from app.routes import events


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    with closing(connect(settings.DATABASE_PATH)) as conn:
        migrate(conn)
    yield


app = FastAPI(title="NEI Events", lifespan=lifespan)
app.include_router(events.router)
