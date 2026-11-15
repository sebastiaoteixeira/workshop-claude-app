from fastapi import APIRouter

from app.db import Conn
from app.repositories import stats
from app.schemas import Health

router = APIRouter(tags=["health"])


@router.get("/health")
def health(conn: Conn) -> Health:
    return Health(**stats.counts(conn))
