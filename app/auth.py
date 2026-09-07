from typing import Annotated

from fastapi import Header

from app import settings
from app.errors import UnauthorizedError


def require_admin(x_admin_token: Annotated[str | None, Header()] = None) -> None:
    if x_admin_token != settings.ADMIN_TOKEN:
        raise UnauthorizedError("invalid admin token")
